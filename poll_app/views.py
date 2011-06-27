#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The module contains all views."""

import logging

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from poll_app.models import Choice, Poll
from poll_app.api import (APIGetRenderer, APIPostRenderer,
APIAllResultsRenderer, APIResultsRenderer)

__author__ = "Gennadiy Zlobin"
__credits__ = ["Gennadiy Zlobin"]
__version__ = "0.0.1"
__maintainer__ = "Gennadiy Zlobin"
__email__ = "gennad.zlobin@gmail.com"
__status__ = "Developing"

logging.basicConfig(level=logging.DEBUG,
        format=('%(filename)s: '
            '%(levelname)s: '
            '%(funcName)s(): '
            '%(lineno)d:\t'
            '%(message)s'))

def index(request):
    """
    Index page.

    Renders an active poll and list of all other polls.
    """
    active_polls = Poll.objects.filter(is_active=True).order_by('pub_date')
    if active_polls:
        active_poll = active_polls[0]
    not_active_polls = Poll.objects.all().order_by('pub_date')
    not_active_polls = list(not_active_polls)

    for i, not_active_poll in enumerate(not_active_polls):
        if not_active_poll == active_poll:
            del not_active_polls[i]

    return render_to_response('polls/index.html',
        {'active_poll': active_poll,
          'not_active_polls': not_active_polls,}
        )

def detail(request, poll_id):
    """
    Renders details of some specific poll.

    Arguments:
        poll_id -- ID of the requested poll.
    """
    p = get_object_or_404(Poll, pk=poll_id)

    # Determine is poll active or not
    p.votable = False
    active_polls = Poll.objects.filter(is_active=True).order_by('pub_date')
    if active_polls:
        active_poll = active_polls[0]
        if active_poll == p:
            p.votable = True

    full_path = request.get_host() + '/api_get' + request.get_full_path()
    return render_to_response('polls/detail.html', {'poll': p, 'full_path':
        full_path}, context_instance=RequestContext(request))

def vote(request, poll_id):
    """
    Vote action.

    Arguments:
        poll_id -- ID of the voted poll.
    """
    p = get_object_or_404(Poll, pk=poll_id)

    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        logging.warning('Choice {0} does not exist', request.POST['choice'])
        return render_to_response('polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        }, context_instance=RequestContext(request))
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('poll_app.views.results',
            args=(p.id,)))

def results(request, poll_id):
    """
    Returns vote results of particular vote.

    Arguments:
        poll_id -- ID of the requested poll.
    """
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/results.html', {'poll': p})

def allresults(request):
    """
    Returns results of all vote.
    """
    polls = Poll.objects.all().order_by('pub_date')
    return render_to_response('polls/allresults.html', {'polls': polls})

def api_get(request, poll_id):
    """
    Returns html of the vote requested by API.

    Arguments:
        poll_id -- ID of the requested poll.
    """
    renderer = APIGetRenderer()
    html = renderer.render(request, poll_id)
    return HttpResponse(html)

def api_post(request, poll_id):
    """
    Vote action requested by API.

    Arguments:
        poll_id -- ID of the voted poll.
    """
    renderer = APIPostRenderer()
    html = renderer.render(request, poll_id)
    return HttpResponse(html)

def api_results(request, poll_id):
    """
    Returns vote results of particular vote requested by API.

    Arguments:
        poll_id -- ID of the requested poll.
    """
    renderer = APIResultsRenderer()
    html = renderer.render(request, poll_id)
    return HttpResponse(html)

def api_allresults(request):
    """
    Returns results of all votes requested by API.
    """
    renderer = APIAllResultsRenderer()
    html = renderer.render(request, poll_id=None)
    return HttpResponse(html)
