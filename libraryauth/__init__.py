'''import logging
from django.conf import settings
from django.http import HttpResponseRedirect
from .views import superlogin

from . import backends

logger = logging.getLogger(__name__)

class Authenticator:
    request=None
    library=None

    def __init__(self, request, library):
        self.request=request
        self.library=library
        
    def process(self, success_url, deny_url):
        logger.info('authenticator for %s at %s.'%(self.request.user, self.library))
        if self.library.has_user(self.request.user):
            return HttpResponseRedirect(success_url)
        backend_test= getattr(backends, self.library.backend + '_authenticate')
        if backend_test(self.request, self.library):
            if self.request.user.is_authenticated():
                self.library.add_user(self.request.user)
                return HttpResponseRedirect(success_url)
            else:
                return superlogin(self.request, extra_context={'library':self.library}, template_name='libraryauth/library_login.html')
            
        else:
            backend_authenticator= getattr(backends, self.library.backend + '_authenticator')
            return backend_authenticator(self.request, self.library, success_url, deny_url)
            
    def allowed(self):
        backend_test= getattr(backends, self.library.backend + '_authenticate')
        return  backend_test(self.request, self.library)
'''