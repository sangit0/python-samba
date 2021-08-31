from flask_restplus import Namespace, fields


class FilesDTO:
    api = Namespace('Samba', description='file related operations')
    file = api.model('file', {
        'name': fields.String(required=True, description='file name'),
        'is_directory': fields.Boolean(required=False),
        'file_size': fields.String(required=False),
        'path': fields.String(required=False),
    })
