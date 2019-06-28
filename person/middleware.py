from django.contrib.sessions.models import Session

class OneSessionPerUser:
    def __init__(self, get_response):
        self.get_response = get_response

    # Compare session_key in database for unique session
    def __call__(self,request):
        if request.user.is_authenticated:
            current_session_key = request.user.logged_in_user.session_key

            # if exists another session, previous session is deleted
            if current_session_key and current_session_key != request.session.session_key:
                Session.objects.get(session_key=current_session_key).delete()
                
            # save the new session
            request.user.logged_in_user.session_key = request.session.session_key
            request.user.logged_in_user.save()

        response= self.get_response(request)

        return response
    
    
