import logging

# NOTE: If you import Resource from flask_restplus_patched, you will get a default OPTIONS method for every GET method you implement.
# The swagger UI it exposes adds no value, so rather than monkey patching, just be careful what you import.
# Original Commit: https://github.com/frol/flask-restplus-server-example/commit/e17bde52a287afa984d6d7eab3f1a63e5c377efe
# --mark
from flask import request
from flask.globals import _request_ctx_stack
from flask_login import current_user
from flask_restplus_patched import Api, reqparse

from egl import config
from egl.db.models.audit_log import AuditLog

logger = logging.getLogger(__name__)
logger.setLevel('INFO')

authorizations = {
    'Basic': {
        'type': 'basic'
    },
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

security = ['Basic', 'Bearer']

api = Api(version='1',
          title='Flask Restplus Demo',
          description='REST APIs demonstrated by 443 Labs.',
          validate=True,
          authorizations=authorizations,
          security=security)

paging_parameters = reqparse.RequestParser()
paging_parameters.add_argument('page', default=1, type=int, help='Current page')
paging_parameters.add_argument('per_page', default=25, type=int, help='Number of items per page')


class PagedResult:
    def __init__(self, items, page, per_page, total):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = total


class Auditable:

    def __init__(self):
        self.user = None

    @property
    def has_request_context(self):
        if _request_ctx_stack is not None:
            if _request_ctx_stack.top is not None:
                return True
        return False

    def audit(self, action, description=None, meta={}, log_message=False) -> AuditLog:
        """
        Builds an AuditLog object, with the current user's username.
        If an http request object is present, the current request will be logged.
        """

        user = current_user or self.user
        assert user

        audit_log_entry = AuditLog()
        audit_log_entry.user_id = user.id
        audit_log_entry.user_email = user.email
        audit_log_entry.action = action
        audit_log_entry.description = description
        audit_log_entry.meta = meta

        try:
            if self.has_request_context:
                audit_log_entry.url = request.url
                firstline = '{} {}'.format(request.method, request.url)

                audit_request_bodies = config.get('AUDIT_REQUEST_BODIES')
                if audit_request_bodies:
                    audit_log_entry.request = '{}\n{}\n{}'.format(firstline, request.headers, request.data)
                else:
                    audit_log_entry.request = '{}\n{}'.format(firstline, request.headers)

            if log_message:
                message = "Audit Log: User: '{}' {}. Meta: {}"
                message = message.format(audit_log_entry.user_email, audit_log_entry.action, audit_log_entry.meta)

                logger.info(message)

        except Exception as e:
            logger.error(e)

        return audit_log_entry

    def get_metadata(self, entity) -> dict:
        meta = {'id': str(entity.id)}

        if hasattr(entity, 'name'):
            meta['name'] = getattr(entity, 'name')

        if hasattr(entity, 'username'):
            meta['username'] = getattr(entity, 'username')

        return meta

    def audit_creation(self, db_model, entity) -> AuditLog:
        """Creates an audit log entry for a create operation."""
        metadata = self.get_metadata(entity)
        return self.audit('Created {}'.format(db_model.__name__), meta=metadata)

    def audit_modification(self, db_model, entity) -> AuditLog:
        """Creates an audit log entry for an update operation."""
        metadata = self.get_metadata(entity)
        return self.audit('Updated {}'.format(db_model.__name__), meta=metadata)

    def audit_deletion(self, db_model, entity) -> AuditLog:
        """Creates an audit log entry for a delete operation."""
        metadata = self.get_metadata(entity)
        return self.audit('Deleted {}'.format(db_model.__name__), meta=metadata)
