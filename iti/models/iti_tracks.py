from odoo import models, fields


class ItiTrack(models.Model):
    _name = 'iti.track'

    name = fields.Char()
    is_open = fields.Boolean()
    capacity = fields.Integer()
    students_ids = fields.One2many('iti.student', 'track_id')

    def name_get(self):
        track_list = []
        for track in self:
            name = track.name
            if track.capacity:
                name += " ({})".format(track.capacity)
            track_list.append((track.id, name))
        return track_list

    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        pass