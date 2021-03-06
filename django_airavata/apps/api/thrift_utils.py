"""
Used to create Django Rest Framework serializers for Apache Thrift Data Types
"""
from thrift.Thrift import TType
from rest_framework.serializers import CharField, BooleanField, DecimalField, IntegerField, Serializer, \
    DictField, SerializerMetaclass, ListField
from django.utils import six
import copy

# used to map apache thrift data types to django serializer fields
mapping = {
    TType.STRING: CharField,
    TType.I08: IntegerField,
    TType.I16: IntegerField,
    TType.I32: IntegerField,
    TType.I64: IntegerField,
    TType.DOUBLE: DecimalField,
    TType.BOOL: BooleanField,
    TType.MAP: DictField
}


def create_serializer(thrift_data_type, **kwargs):
    """
    Create django rest framework serializer based on the thrift data type
    :param thrift_data_type: Thrift data type
    :param kwargs: Other Django Framework Serializer initialization parameters
    :return: instance of custom serializer for the given thrift data type
    """
    return create_serializer_class(thrift_data_type)(**kwargs)

def create_serializer_class(thrift_data_type):
    class CustomSerializerMeta(SerializerMetaclass):

        def __new__(cls, name, bases, attrs):
            meta = attrs.get('Meta', None)
            thrift_spec = thrift_data_type.thrift_spec
            for field in thrift_spec:
                # Don't replace existing attrs to allow subclasses to override
                if field and field[2] not in attrs:
                    required = field[2] in meta.required if meta else False
                    read_only = field[2] in meta.read_only if meta else False
                    allow_null = not required
                    field_serializer = process_field(
                        field, required=required, read_only=read_only,
                        allow_null=allow_null)
                    attrs[field[2]] = field_serializer
            return super().__new__(cls, name, bases, attrs)

    @six.add_metaclass(CustomSerializerMeta)
    class CustomSerializer(Serializer):
        """
        Custom Serializer which handle the list fields which holds custom class objects
        """

        def process_nested_fields(self, validated_data):
            fields = self.fields
            params = copy.deepcopy(validated_data)
            for field_name, serializer in fields.items():
                if isinstance(serializer, ListField):
                    if (params[field_name] is not None or not serializer.allow_null):
                        if isinstance(serializer.child, Serializer):
                            params[field_name] = [serializer.child.create(item) for item in params[field_name]]
                        else:
                            params[field_name] = serializer.to_representation(params[field_name])
                elif isinstance(serializer, Serializer):
                    params[field_name] = serializer.create(params[field_name])
            return params

        def create(self, validated_data):
            params = self.process_nested_fields(validated_data)
            return thrift_data_type(**params)

        def update(self, instance, validated_data):
            raise Exception("Not implemented")

    return CustomSerializer


def process_field(field, required=False, read_only=False, allow_null=False):
    """
    Used to process a thrift data type field
    :param field:
    :param required:
    :param read_only:
    :param allow_null:
    :return:
    """
    if field[1] in mapping:
        # handling scenarios when the thrift field type is present in the
        # mapping
        field_class = mapping[field[1]]
        kwargs = dict(required=required, read_only=read_only)
        # allow_null isn't allowed for BooleanField
        if field_class not in (BooleanField,):
            kwargs['allow_null'] = allow_null
        # allow_null CharField are also allowed to be blank
        if field_class == CharField:
            kwargs['allow_blank'] = allow_null
        return mapping[field[1]](**kwargs)
    elif field[1] == TType.LIST:
        # handling scenario when the thrift field type is list
        list_field_serializer = process_list_field(field)
        return ListField(child=list_field_serializer,
                         required=required,
                         read_only=read_only,
                         allow_null=allow_null)
    elif field[1] == TType.STRUCT:
        # handling scenario when the thrift field type is struct
        return create_serializer(field[3][0],
                                 required=required,
                                 read_only=read_only,
                                 allow_null=allow_null)


def process_list_field(field):
    """
    Used to process thrift list type field
    :param field:
    :return:
    """
    list_details = field[3]
    if list_details[0] in mapping:
        # handling scenario when the data type hold by the list is in the
        # mapping
        return mapping[list_details[0]]()
    elif list_details[0] == TType.STRUCT:
        # handling scenario when the data type hold by the list is a struct
        return create_serializer(list_details[1][0])
