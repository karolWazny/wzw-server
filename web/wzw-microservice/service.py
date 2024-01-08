# Server for E-Xsultate Songbook Generator Service
# Copyright (C) 2022  Karol Ważny

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

class Service:
    def __init__(self, job_controller):
        self.job_controller = job_controller

    def get_requested_format(self, job_id: str) -> str:
        return self.job_controller.get_job_metadata(job_id)['format']

    def order_song_classification(self, job_data):
        return self.job_controller.enqueue_job(job_data, 'queue:wzw')


    def order_pdf_generation(self, job_data):
        return self.job_controller.enqueue_job(job_data, 'queue:wzw', metadata={'format': 'pdf'})

    def job_status(self, job_id):
        return self.job_controller.job_status(job_id)

    def fetch_result(self, job_id):
        return self.job_controller.fetch_job_result(job_id)
