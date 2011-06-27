#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The module contains classes for API rendering."""

from django.shortcuts import get_object_or_404
from django.template import Context
from django.template.loader import get_template

from poll_app.models import Poll

__author__ = "Gennadiy Zlobin"
__credits__ = ["Gennadiy Zlobin"]
__version__ = "0.0.1"
__maintainer__ = "Gennadiy Zlobin"
__email__ = "gennad.zlobin@gmail.com"
__status__ = "Developing"

class APIRenderer:
    """Absract base class."""
    def render(request, poll_id=None):
        """
        Returns rendered html.

        Arguments:
            poll_id -- ID of the requested poll.
        """
        raise NotImplementedError()

class APIGetRenderer(APIRenderer):
    """Hanlder for get requests rendering."""
    def render(self, request, poll_id=None):
        """
        Returns rendered html.

        Arguments:
            poll_id -- ID of the requested poll.
        """
        import pdb; pdb.set_trace()
        p = get_object_or_404(Poll, pk=poll_id)
        p.votable = False
        active_polls = Poll.objects.filter(is_active=True).order_by('pub_date')
        if active_polls:
            active_poll = active_polls[0]
            if active_poll == p:
                p.votable = True

        full_path = request.get_host() + request.get_full_path()
        t = get_template('polls/api_detail.html')
        c = Context({'poll': p, 'full_path': full_path})
        return t.render(c)

class APIPostRenderer(APIRenderer):
    """Hanlder for vote requests rendering."""
    def render(self, request, poll_id=None):
        """
        Returns rendered html.

        Arguments:
            poll_id -- ID of the requested poll.
        """
        p = get_object_or_404(Poll, pk=poll_id)
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
        selected_choice.votes += 1
        selected_choice.save()

        t = get_template('polls/api_results.html')
        c = Context({'poll': p})
        return t.render(c)

class APIResultsRenderer(APIRenderer):
    """Hanlder for particular vote results requests rendering."""
    def render(self, request, poll_id=None):
        """
        Returns rendered html.

        Arguments:
            poll_id -- ID of the requested poll.
        """
        p = get_object_or_404(Poll, pk=poll_id)
        t = get_template('polls/api_results.html')
        c = Context({'poll': p})
        return t.render(c)

class APIAllResultsRenderer(APIRenderer):
    """Hanlder for all results requests rendering."""
    def render(self, request, poll_id=None):
        """
        Returns rendered html.

        Arguments:
            poll_id -- ID of the requested poll.
        """
        polls = Poll.objects.all().order_by('pub_date')
        t = get_template('polls/api_allresults.html')
        c = Context({'polls': polls})
        return t.render(c)
