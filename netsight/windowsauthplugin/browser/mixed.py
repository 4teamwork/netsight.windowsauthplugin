from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from urlparse import parse_qs
from urlparse import urlparse


class SPNEGOChallengeJSView(BrowserView):

    def __call__(self):
        """Challenge the user for credentials before returning javascript.
        """
        response = self.request.response

        # Set no-cache headers
        response.setHeader('Cache-Control',
                           'no-cache, no-store, must-revalidate')
        response.setHeader('Pragma', 'no-cache')
        response.setHeader('Expires', '0')

        # Select response
        mtool = getToolByName(self.context, 'portal_membership')
        if mtool.isAnonymousUser():
            response.addHeader('WWW-Authenticate', 'Negotiate')
            response.addHeader('Connection', 'keep-alive')
            response.addHeader('Content-Type', 'text/javascript')
            response.setStatus(401)
            return u"/* You are not authorized to access this resource. */"
        elif not bool(self.request.response.cookies):
            return u"/* Authentication cookie was not set. Cannot redirect. */"
        else:
            # Return Javascript to redirect and continue login process
            qs = urlparse(self.request.get('HTTP_REFERER', '')).query
            query_params = parse_qs(qs)
            portal_url = self.context.portal_url()
            return "window.location.replace('%s/logged_in?came_from=%s')" % (
                portal_url,
                query_params.get('came_from', [portal_url])[0])
