# Copyright 2012 OpenStack LLC.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from sqlalchemy import Boolean, Column, DateTime, BigInteger
from sqlalchemy import MetaData, Integer, String, Table

from cinder.openstack.common import log as logging

LOG = logging.getLogger(__name__)


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    # add column:
    bw_usage_cache = Table('bw_usage_cache', meta, autoload=True)
    uuid = Column('uuid', String(36))

    # clear the cache to get rid of entries with no uuid
    migrate_engine.execute(bw_usage_cache.delete())

    bw_usage_cache.create_column(uuid)


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    # drop column:
    bw_usage_cache = Table('bw_usage_cache', meta,
        Column('created_at', DateTime(timezone=False)),
        Column('updated_at', DateTime(timezone=False)),
        Column('deleted_at', DateTime(timezone=False)),
        Column('deleted', Boolean(create_constraint=True, name=None)),
        Column('id', Integer(), primary_key=True, nullable=False),
        Column('mac', String(255)),
        Column('uuid', String(36)),
        Column('start_period', DateTime(timezone=False), nullable=False),
        Column('last_refreshed', DateTime(timezone=False)),
        Column('bw_in', BigInteger()),
        Column('bw_out', BigInteger()),
        useexisting=True)

    bw_usage_cache.drop_column('uuid')
