from flask import request
from flask_restplus import Resource
from ..util.dto import FilesDTO
from ..service.samba_service import change_password, get_file_list, download_normal,download_using_file_writter, create_user_using_ssh,create_user_using_command
from flask import send_file
from flask import current_app
from ..service.decode_service import decode_url, encode_url

api = FilesDTO.api
_files = FilesDTO.file

request_parser_access = api.parser()
request_parser_access.add_argument('username', help='username', required=True, location=('form', 'values','json'))
request_parser_access.add_argument('password', help='password', required=True, location=('form', 'values','json'))
request_parser_access.add_argument('path', help='path', required=True, location=('form', 'values','json'))
request_parser_access.add_argument('user_folder', help='user_folder', required=True, location=('form', 'values','json'))


user_request = api.parser()
user_request.add_argument('username', help='username', required=True, location=('form', 'values','json'))
user_request.add_argument('password', help='password', required=True, location=('form', 'values','json'))
user_request.add_argument('user_folder', help='user_folder', required=True, location=('form', 'values','json'))

download_request = api.parser()
download_request.add_argument('url', help='url', required=True, location=('form', 'values','json'))


@api.route('/files')
class GetFile(Resource):
    @api.marshal_list_with(_files, envelope='data')
    @api.doc('list_of_files')
    @api.expect(request_parser_access)
    def post(self):
        """List all samba files"""
        try:
            username = request_parser_access.parse_args()['username']
            password = request_parser_access.parse_args()['password']
            user_folder = request_parser_access.parse_args()['user_folder']
            path = request_parser_access.parse_args()['path']

            return get_file_list(username,password,user_folder,path)
        except Exception as e:
            api.abort(400,  e)

@api.route('/download-file')
class GetFileDownloadSecure(Resource):
    @api.doc('download-file')
    @api.expect(download_request)
    def get(self):
        """download samba file"""
        try:
            url = download_request.parse_args()['url']
            decoded_url = decode_url(url)
            return send_file("/sambashares/"+decoded_url,as_attachment=True)
        except PermissionError as e:
            api.abort(403,  e)     
        except Exception as e:
            api.abort(404,  "File not found! Can't download")
    
    @api.doc('request url')
    @api.expect(request_parser_access)
    def post(self):
        """request samba file"""
        try:
            username = request_parser_access.parse_args()['username']
            password = request_parser_access.parse_args()['password']
            user_folder = request_parser_access.parse_args()['user_folder']
            path = request_parser_access.parse_args()['path']

            filename = path
            response = download_normal(username,password,user_folder,[filename])
            base_path = current_app.config["SAMBA_BACKEND_PYTHON"] +"/download-file?url="
            token = encode_url(username,user_folder,path)

            if response : 
                return { 'url': f"{base_path}{token}" }
            api.abort(403,  "Not downloaded url error")
        except Exception as e:
            api.abort(400,  e)
        
        

@api.route('/download-with-file-writter')
class GetFileDownload(Resource):
    @api.doc('download-with-file-writter')
    @api.expect(request_parser_access)
    def get(self):
        try:
            username = request_parser_access.parse_args()['username']
            password = request_parser_access.parse_args()['password']
            user_folder = request_parser_access.parse_args()['user_folder']
            path = request_parser_access.parse_args()['path']

            filename = path
            response = download_using_file_writter(username,password,user_folder,[filename])
            if response : 
                return send_file('downloads/'+filename,
                        as_attachment=True)
            api.abort(403,  "Not downloaded url error")
        except Exception as e:
            api.abort(400,  e)

@api.route('/create-user')
class CreateUseer(Resource):
    @api.doc('create-user')
    @api.expect(user_request)
    def post(self):
         try:
            username = user_request.parse_args()['username']
            password = user_request.parse_args()['password']
            user_folder = user_request.parse_args()['user_folder']
            create_user_using_command(username,password,user_folder)
            response_object = {
                    'status': 'done',
            }
            return response_object, 200
         except Exception as e:
            api.abort(400,  e)
@api.route('/update-password')          
class UpdatePassword(Resource):
    @api.doc('update-password')
    @api.expect(user_request)
    def post(self):
         try:
            username = user_request.parse_args()['username']
            password = user_request.parse_args()['password']
            change_password(username,password)
            response_object = {
                    'status': 'done',
            }
            return response_object, 200
         except Exception as e:
            api.abort(400,  e)
     