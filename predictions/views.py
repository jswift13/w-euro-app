# predictions/views.py
from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.forms import formset_factory
from django.utils import timezone

from fixtures.models import Matchday
from .forms import PredictionForm, MatchPickForm, BaseMatchPickFormSet
from .models import Prediction, MatchPick
from django.db.models import Count
from django.shortcuts import redirect
from django.db.models import Max

def home(request):
    now = timezone.now()
    # annotate each Matchday with its last kickoff time
    md = (
        Matchday.objects
        .annotate(last_kickoff=Max('matches__kickoff_time'))
        .filter(last_kickoff__gte=now)
        .order_by('order')
        .first()
    )
    if not md:
        # no upcoming MDs? show the most recent one
        md = (
            Matchday.objects
            .annotate(last_kickoff=Max('matches__kickoff_time'))
            .order_by('-last_kickoff')
            .first()
        )
    # redirect into your existing create_prediction flow
    return redirect('predictions:create', matchday_id=md.pk)

def create_prediction(request, matchday_id):
    all_mds = Matchday.objects.order_by('order')
    # Ensure session key exists
    if not request.session.session_key:
        request.session.create()
    sk = request.session.session_key

    matchday = get_object_or_404(Matchday, pk=matchday_id)
    matches  = matchday.matches.order_by('kickoff_time')
    first_match = matches.first()
    first_kickoff = first_match.kickoff_time if first_match else None

    # Check for an existing prediction this session+matchday
    existing = Prediction.objects.filter(
        matchday=matchday,
        session_key=sk
    ).first()

    # Build the formset factory
    MatchPickFormSet = formset_factory(
        MatchPickForm,
        formset=BaseMatchPickFormSet,
        extra=len(matches),
        max_num=len(matches),
    )

    if request.method == 'POST':
        # On POST, bind either to existing or new
        p_form = PredictionForm(
            request.POST,
            instance=existing,
            matchday=matchday
        )
        pick_formset = MatchPickFormSet(
            request.POST,
            matches=matches
        )

        if p_form.is_valid() and pick_formset.is_valid():
            # Save or update Prediction
            prediction = p_form.save(commit=False)
            prediction.matchday   = matchday
            prediction.session_key = sk
            prediction.save()

            # Clear old picks if updating
            MatchPick.objects.filter(prediction=prediction).delete()

            # Save new picks before kickoff
            now = timezone.now()
            for pick_form in pick_formset:
                if now < pick_form.match.kickoff_time:
                    cd = pick_form.cleaned_data
                    home = cd.get('predicted_home_score')
                    away = cd.get('predicted_away_score')
                    if home is not None and away is not None:
                        MatchPick.objects.create(
                            prediction=prediction,
                            match=pick_form.match,
                            predicted_home_score=home,
                            predicted_away_score=away,
                        )
            return redirect('predictions:confirmation', pk=prediction.pk)

    else:
        # On GET: prefill if existing
        p_form = PredictionForm(
            instance=existing,
            matchday=matchday
        )
        # Build initial data for the formset
        initial = []
        for match in matches:
            pick = (
                existing.picks.filter(match=match).first()
                if existing else None
            )
            if pick:
                initial.append({
                    'predicted_home_score': pick.predicted_home_score,
                    'predicted_away_score': pick.predicted_away_score,
                })
            else:
                initial.append({})
        pick_formset = MatchPickFormSet(
            initial=initial,
            matches=matches
        )

    pairs = zip(matches, pick_formset.forms)
    return render(request, 'predictions/prediction_form.html', {
        'matchdays': all_mds,
        'matchday': matchday,
        'form':      p_form,
        'formset':   pick_formset,
        'pairs':     pairs,
        'first_kickoff': first_kickoff,
        'existing': existing,   # to let the template show “Edit your picks”
    })


def confirmation(request, pk):
    prediction = get_object_or_404(Prediction, pk=pk)
    return render(request, 'predictions/confirmation.html', {
        'prediction': prediction
    })




def about(request):
    # TODO: flesh out your “About the App” copy
    return render(request, 'predictions/about.html')

def standings(request):
    # Top 5 favorite teams
    favs = Prediction.objects.values('favorite_team__name') \
                .annotate(count=Count('favorite_team')) \
                .order_by('-count')[:5]

    # Top 5 POTMs
    pots = Prediction.objects.values('potm__name') \
                .annotate(count=Count('potm')) \
                .order_by('-count')[:5]

    return render(request, 'predictions/standings.html', {
        'favs': favs,
        'pots': pots,
    })