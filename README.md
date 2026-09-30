# Storyblok Showcase Demo (Solution Engineers)

This repository is the **Showcase** frontend for Storyblok Solution Engineers.
It is the place for experimental, edge-case, and specialized demo features that
are not (yet) part of the standard SE demo. It is built using
[Nuxt 4](https://nuxt.com/) and [TailwindCSS](https://tailwindcss.com/).

> The repository is <https://github.com/storyblok/storyblok-demo-showcase-se>.
> It is forked from the Default SE Demo
> <https://github.com/storyblok/storyblok-demo-default-se>, which in turn is
> forked from the Joyful Demo <https://github.com/storyblok/storyblok-demo-default-v2>.

Feel free to explore and reuse the code, but please be aware of the
[demo-specific implementation practices](#demo-specific-implementation-notes),
which deviate from the most common implementation practices.

## Default Demo vs Showcase

The SE demo work is split across two repositories:

| | Default Demo (`storyblok-demo-default-se`) | Showcase (this repository) |
| --- | --- | --- |
| Purpose | Stable baseline for standard and custom demos | Playground for experimental, advanced, or specialized features |
| Used by | Every new SE demo space by default | Demos that need a feature not available in the Default Demo |
| Stability | Stable. Pull requests need at least two reviewers or testers | Experimental. Features are validated here before promotion |
| Content | Generic components for most prospects | Edge cases, industry-specific components, integrations, mock data |

Start from the **Default Demo** unless the work involves significant custom
component development or a feature that already lives in Showcase.

Features in Showcase can be **promoted to the Default Demo** when, after team
review, they are stable and broadly relevant.

### Not sure where a feature belongs?

Do not overthink it. Open an issue in the
[Default Demo repository](https://github.com/storyblok/storyblok-demo-default-se/issues)
first. The team evaluates together whether the feature belongs in the Default
Demo or in Showcase, based on how broadly it applies.

## What belongs in Showcase

Good candidates for this repository:

- advanced or alternative implementations of existing features, for example
  the FAQ section by reference;
- integrations and connectors under development, for example the SAP connector;
- A/B testing and experimentation scenarios;
- dynamic branding and theme-switching scenarios, for example multi-brand
  setups where colors, prices, or content change based on brand or location;
- industry- or segment-specific components, for example sport components that
  load player data from an external source;
- mock data used to demo external data integrations;
- specific content models, for example an internal user portal.

Keep in the Default Demo anything that most demos need: brand expression,
generic page sections, navigation, and common content types.

## Workflow for custom development

### Customer-specific work

For an immediate customer requirement, keep the fast workflow and implement the
new component in the Default Demo:

1. Clone the [Default Demo repository](https://github.com/storyblok/storyblok-demo-default-se).
2. Create a branch named `feat/<your-change>`, for example
   `feat/rate-comparison-table`. Name it after the feature, not the customer.
3. Build what the demo needs and test it locally against the demo space (see
   [Run locally](docs/run-locally.md)).
4. Push the branch and open a pull request against the `main` branch of the
   Default Demo. The pull request triggers a Netlify/Vercel deploy on a
   dedicated hostname. The deploy link is available in the pull request.
5. Use that deploy URL as the Visual Editor preview URL of the customer demo
   space (see [Point a Default Demo space at the Showcase frontend](#point-a-default-demo-space-at-the-showcase-frontend)).

The pull request stays open while you use it for the demo. It is merged into
the Default Demo only if the component is evaluated as reusable, as described
below.

### Bring your implementation into Showcase

If you want your implementation to live in Showcase instead, open a pull request
on the [Showcase repository](https://github.com/storyblok/storyblok-demo-showcase-se).
After review, it is merged into Showcase.

### After the demo: evaluate for reuse

Custom code built for one customer is usually thrown away after the demo. Before
you discard it, ask:

- Does this component help a prospect understand Storyblok's value better than
  the existing components?
- Is the need likely to appear again for other customers in the same segment,
  industry, or business model?
- Can it be configured through Storyblok fields instead of being hard-coded for
  one brand, campaign, layout, or dataset?
- Can the naming, schema, design, and responsive behavior be generic enough for
  other SEs to reuse without rewriting it?

If the answer is yes:

1. Announce the component in the team channel to gauge interest.
2. Clean up hardcoded values and customer-specific content.
3. Open an issue (see [Not sure where a feature belongs?](#not-sure-where-a-feature-belongs))
   describing:
   - the demo scenario it solves;
   - the expected Storyblok component schema and fields;
   - how content editors will use it;
   - design-token, responsive, and Visual Editor requirements;
   - whether it depends on external services, mock data, or demo-space
     configuration.
4. After the approach is agreed, implement it in Showcase or in the Default
   Demo, add or update the related Storyblok schema and configuration, test it
   locally against a demo space, and open a pull request.

## Access the Showcase demo space

For now, the Showcase demo is a single shared Storyblok space, not a template.
Open it, or request access if you do not have it yet:

<https://app.storyblok.com/#/me/spaces/295576087731079/dashboard>

This space already contains the Showcase components, schemas, and content, and
points at the Showcase frontend.

In the near future, the Showcase demo will be available as a template, like the
Default Demo, so you can generate your own Showcase space from
<https://app.storyblok.com/#/me/spaces/new?tab=experience-demo>.

### Point a Default Demo space at the Showcase frontend

Until the template is available, you can also point a Default Demo space at the
Showcase frontend. Create the space as described in the
[Default Demo repository](https://github.com/storyblok/storyblok-demo-default-se),
then:

1. Disable the default demo option in
   `Settings > Maintenance Mode > Enable example mode`.
2. Add the Showcase frontend URL in `Settings > Visual Editor > Location` or
   through **Add Preview URLs**:

```text
https://YOUR-SHOWCASE-FRONTEND-URL/?token=YOURSPACEPREVIEWACCESSTOKEN&path=
```

Replace `YOUR-SHOWCASE-FRONTEND-URL` with the deployed Showcase frontend or your
local URL, and `YOURSPACEPREVIEWACCESSTOKEN` with the space's Preview access
token from `Settings > Access Tokens`.

Showcase features that need extra components or fields also need the matching
Storyblok schema in the space. A Default Demo space does not include them.

## Run locally

Run the frontend locally when you need to build, test, or preview code against a
specific Storyblok demo space.

For the technical setup steps, see [Run locally](docs/run-locally.md).

## Demo-Specific implementation notes

### Access token and path via URL parameters

We needed one deployed environment that could be used to display a large number of demo spaces that are generated on the fly. Therefore, the access tokens of these spaces are passed via URL parameters. In a more typical scenario, you would probably want to manage the access token as an environment variable. See the note in `nuxt.config.ts` and delete `app/plugins/storyblok.js` to remove the extra functionality for tokens as URL parameters altogether.

### Internationalization and language detection

For the demo, it has to be possible for any language to be added to the internationalization settings in Storyblok and detected automatically on the front end. All currently active language codes are retrieved from the Storyblok space to ensure this. When fetching a particular story based on the current route, it is checked whether any of the currently active language codes matches the first part of the route. For example, if the current route was `https://localhost:3000/de/home` and German had been added as a language, `de` would get added as the language parameter in the API request for the home story. You can look at the [getLanguage composable](app/composables/getLanguage.js) to see how it works. In a real-world project, you would usually know which languages are used on the website, allowing you to choose a simpler approach.

### Setting a real path for stories

The main drawback of handling internationalization as described above is that field-level translation will not work when setting a real path for certain stories (e.g., `/` instead of `home`). When setting a real path, the language code is no longer part of the route, thus making it impossible to detect.
