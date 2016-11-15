class FlagUpdateView(UpdateView):
    """ Update flagged post."""
    model = PostMarkType
    form_class = PostMarkTypeForm
    template_name = 'admin/flag-update.html'
    success_url = reverse_lazy('flag-list')

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(FlagUpdateView, self).dispatch(*args, **kwargs)


class FlagList(ListView):
    """ List of flagged posts."""
    model = PostMarkType
    template_name = 'admin/flag-list.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(FlagList, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        return super(FlagList, self).get_queryset().filter(reviewed=True)


class SponsorEditView(LoginRequiredMixin, UpdateView):
    model = Sponsor
    form_class = SponsorEditForm
    template_name = 'sponsor/edit.html'

    def get_context_data(self, **kwargs):
        context = super(SponsorEditView, self).get_context_data(**kwargs)
        context['edit_mode'] = True
        return context

    def get_success_url(self):
        return reverse('sponsors:detail', args=[self.object.pk])


class SponsorPageView(LoginRequiredMixin, DetailView):
    model = Sponsor
    template_name = 'sponsor/detail.html'

    def get_context_data(self, **kwargs):
        context = super(SponsorPageView, self).get_context_data(**kwargs)
        context.update(group_type='sponsor')
        return context


class FollowersView(LoginRequiredMixin, DetailView):
    model = Sponsor
    template_name = 'sponsor/followers.html'


class TopPostView(LoginRequiredMixin, DetailView):
    model = Sponsor
    template_name = 'sponsor/top_posts.html'

    def get_context_data(self, **kwargs):
        context = super(TopPostView, self).get_context_data(**kwargs)
        context['top_posts'] = self.object.post_set.annotate(
            inspire_count=Count('inspire')).order_by('-inspire_count')[:5]
        return context