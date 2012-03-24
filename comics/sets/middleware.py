import datetime

from comics.sets.models import Set

class SetMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        For set views do the following on the session object:
        - Maintain last_visit and this_visit, such that a "Since last visit"
          time frame may be offered the user in the menu.
        - Add the current set to recent_sets list.
        """

        if 'set' in view_kwargs and hasattr(request, 'session'):
            session = request.session

            # Create last_visit
            if not 'last_visit' in session:
                session['last_visit'] = datetime.date.today()

            # Update last_visit
            if ('this_visit' in session
                and session['this_visit'] < datetime.date.today()
                and session['last_visit'] != session['this_visit']):
                session['last_visit'] = session['this_visit']

            # Create/update this_visit
            if (not 'this_visit' in session
                or session['this_visit'] < datetime.date.today()):
                session['this_visit'] = datetime.date.today()

            try:
                # Update 'last loaded' time stamp on the set
                set = Set.objects.get(name=view_kwargs['set'])
                set.set_loaded()

                # Add set to recent_sets in the session
                if not 'recent_sets' in session:
                    session['recent_sets'] = [set.name]
                elif not set in session['recent_sets']:
                    session['recent_sets'].append(set.name)
                    # Since we only modified a list in the session and not
                    # the session object itself, we must mark the session
                    # as modified to have the changes saved
                    session.modified = True
            except Set.DoesNotExist:
                pass

        return None
