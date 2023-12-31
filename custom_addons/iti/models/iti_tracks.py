from odoo import models, fields, api


class ItiTrack(models.Model):
    _name = 'iti.track'

    name = fields.Char()
    is_open = fields.Boolean()
    capacity = fields.Integer()
    students_ids = fields.One2many('iti.student', 'track_id')

    # def name_get(self):
    #     track_list = []
    #     for track in self:
    #         name = track.name
    #         if track.capacity:
    #             name += " ({})".format(track.capacity)
    #         track_list.append((track.id, name))
    #     return track_list
    #
    # def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
    #     pass
    @api.model
    def name_create(self, name):
        print("Self ", self)
        print("Track Name ", name)
        # rec = self.create({'name':name})
        # print("rec", rec)
        vals = {
            'name': name,
            'is_open': True,
            'capacity': 20
        }
        return self.create(vals).name_get()[0]

    @api.model
    def default_get(self, fields_list):
        rec = super().default_get(fields_list)
        rec['is_open'] = True
        rec['capacity'] = 20
        print("Return Statement", rec)
        return rec
