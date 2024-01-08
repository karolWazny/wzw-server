# Server for E-Xsultate Songbook Generator Service
# Copyright (C) 2022  Karol Ważny
import io

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import quart
import logging

async_generator_service = None

application = quart.Quart(__name__)


@application.route('/', methods=['GET'])
def home():
    return "<p>This is not a website server. It only provides microservices.</p>"


@application.route('/api/v1/wzw/classified/<identifier>', methods=['GET'])
async def get_job_result(identifier):
    result = async_generator_service.fetch_result(identifier)
    if result is None:
        return quart.jsonify({
            'message': "There is no generated file with given identifier",
            "identifier": identifier
        }), 404
    else:
        result = async_generator_service.fetch_result(identifier)
        result_format = async_generator_service.get_requested_format(identifier)
        return await quart.send_file(
            result,
            as_attachment=True,
            attachment_filename='songbook.' + result_format
            #mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )


@application.route('/api/v1/wzw/status', methods=['GET'])
async def get_job_status():
    identifier = quart.request.args.get('identifier')
    status = async_generator_service.job_status(identifier)
    if status is None:
        return quart.jsonify({
            'message': "No job with such identifier",
            "identifier": identifier
        }), 404
    else:
        return {
            "identifier": identifier,
            "status": status
        }


@application.route('/api/v1/wzw', methods=['POST'])
async def schedule_async_job():
    files = await quart.request.files
    parts = await quart.request.form
    file = io.BytesIO()
    await files['audio'].save(file)
    logging.info(files.keys())
    logging.info(parts['lyrics'])

    # if songbook_format == 'docx':
    #     logging.info('enqueuing docx job')
    #     logging.debug('job: ' + str(data))
    #     identifier = async_generator_service.order_docx_generation(data)
    # elif songbook_format == 'pdf':
    #     logging.info('enqueuing pdf job')
    #     logging.debug('job: ' + str(data))
    #     identifier = async_generator_service.order_pdf_generation(data)
    # else:
    #     return quart.jsonify({
    #         'message': "Requested songbook format: {0} is not supported.\n"
    #                    "Supported formats are: pdf, docx.".format(songbook_format)
    #     }), 400
    return quart.jsonify({
        'identifier': '123qwe'
    }), 201
