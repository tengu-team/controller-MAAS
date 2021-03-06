# !/usr/bin/env python3
# Copyright (C) 2016  Qrama
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# pylint: disable=c0111,c0301,c0325, r0903,w0406

from os import remove
from shutil import copyfile

from charms.reactive import when, when_not, set_state, remove_state
from charmhelpers.core.hookenv import status_set, charm_dir
from charmhelpers.core.host import service_restart, chownr


@when('sojobo.available')
@when_not('controller-maas.installed')
def install(sojobo):
    api_dir = list(sojobo.connection())[0]['api-dir']
    copyfile('{}/files/controller_maas.py'.format(charm_dir()), '{}/controllers/controller_maas.py'.format(api_dir))
    chownr(api_dir, 'sojobo', 'www-data', chowntopdir=True)
    service_restart('nginx')
    status_set('active', 'data copied')
    set_state('controller-maas.installed')


@when('sojobo.removed')
def remove_controller(sojobo):
    api_dir = list(sojobo.connection())[0]['api-dir']
    remove('{}/controllers/controller_maas.py'.format(api_dir))
    service_restart('nginx')
    remove_state('controller-maas.installed')
