# Storyblok Solution Engineers Demo

This frontend is used when you [create a new demo space (for **Solution Engineers**) in Storyblok](https://app.storyblok.com/#/me/spaces/new?tab=experience-demo). It is built using [Nuxt 4](https://nuxt.com/) and [TailwindCSS](https://tailwindcss.com/).

> The repository is <https://github.com/storyblok/storyblok-demo-default-se> . It is a forked repository from the JoyFul Demo <https://github.com/storyblok/storyblok-demo-default-v2>

Feel free to explore and reuse the code, but please be aware of the [demo-specific implementation practices](#demo-specific-implementation-notes), which deviate from the most common implementation practices.

## Choose the right demo workflow

There are three common workflows for this Base Demo:

- Create a new Base Demo space when you only need to customize content and
  Storyblok space configuration.
- Create a new Base Demo space and run this frontend locally when you need
  prospect-specific custom components.
- Propose a new reusable component for the shared Base Demo so other developers
  and SEs can use it in future spaces.

## Create a new Base Demo space

You do not need to clone, install, or deploy this repository to create a new SE
demo instance. Storyblok creates a new demo space with demo content and points
it at the shared deployed frontend.

1. Go to <https://app.storyblok.com/#/me/spaces/new?tab=experience-demo>

2. Under **Choose your demo theme**, select **Solutions Theme** (`Solutions Demo Environment`).

3. Fill in the **Space name**, for example `My Demo`.

4. For **Do you want to assign the space to your organization?** choose **Yes (visible to everyone in the organization)**. This is the important one: it puts the space in the Storyblok demo Organization, which is on the **Elite plan**, so the space gets all Elite features. It also means colleagues can open and reuse it. Picking **No** creates a private space outside that organization, without the Elite plan.

5. Click **Explore Demo Space**.

The filled-in form looks like this:

![Creating a new Solutions demo space in Storyblok](docs/create-demo-space.png)

The space is created with demo content already in place and pointing at the
deployed frontend, so there is nothing else to configure for the default demo
flow. Open the generated space and start from the **Home** story.

Use this workflow when you need to customize content and space configuration
only, for example:

- changing colors, fonts, header navigation, footer content, and other global
  options in the `site-config` story;
- creating roles and permissions;
- configuring custom workflows;
- uploading assets;
- changing content, folders, datasources, languages, or Visual Editor settings.

If you need to set or repair the Visual Editor preview URL manually, use:

```text
https://storyblok-demo-default-se.netlify.app/?token=YOURSPACEPREVIEWACCESSTOKEN&path=
```

Replace `YOURSPACEPREVIEWACCESSTOKEN` with the space's Preview access token
from `Settings > Access Tokens`, then add the URL in
`Settings > Visual Editor > Location` or through **Add Preview URLs**.

### Use a custom preview URL

A small variation of the default workflow is creating a Base Demo space but
pointing the Visual Editor at a different frontend URL. In that case, remove the
default demo option from `Settings > Maintenance Mode > Enable example mode`
and configure a new preview URL in `Settings > Visual Editor > Location` or
through **Add Preview URLs**.

Use the same query-parameter pattern:

```text
https://YOUR-FRONTEND-URL/?token=YOURSPACEPREVIEWACCESSTOKEN&path=
```

Replace `YOUR-FRONTEND-URL` with your deployed or local frontend URL, and
replace `YOURSPACEPREVIEWACCESSTOKEN` with the space's Preview access token.

## Create a Base Demo with custom components

Use this workflow when a prospect demo needs frontend behavior or presentation
that does not exist in the shared Base Demo yet. In this case, create the demo
space first, then run this frontend locally while building and testing the
custom component.

## Run locally

To run the demo locally, follow these steps:

1. Clone the repository and install dependencies:

```bash
npm install
```

2. Create an `.env` file with your preview access token (find it under `Settings > Access Tokens` in your Storyblok space):

```bash
STORYBLOK_TOKEN=your-preview-access-token
```

3. Next, run the development server:

```bash
npm run dev
```

To run the development server with HTTPS (required for Storyblok Visual Editor):

1. Install `mkcert` if you haven't already:
   ```bash
   brew install mkcert
   ```

2. Install the local CA certificate in your system trust store:
   ```bash
   mkcert -install
   ```

3. Generate SSL certificates for localhost:
   ```bash
   mkcert localhost
   ```
   This creates two files in your project root:
   - `localhost.pem` (certificate)
   - `localhost-key.pem` (private key)

4. Run the development server with HTTPS:
   ```bash
   npm run devs
   ```

The HTTPS configuration is set up in `nuxt.config.ts` using the generated certificate files. The server will be available at `https://localhost:3000`.

> Note: if you want to use Bun or some other runtime/packagemanager you can replace `npm` with the proper command, for example `bun install` and `bun run devs`

In your Storyblok space, go to `Settings` > `Visual Editor > Location` or use
**Add Preview URLs**, then set `https://localhost:3000/?token=YOURSPACEPREVIEWTOKEN&path=`.
Replace `YOURSPACEPREVIEWTOKEN` with your Space Preview access token.
Next go to `Settings` > `Maintenance Mode` and disable `Example Mode`. This will ensure that the preview URL you just set can be used in the visual editor.

Finally, open your **Home** story and see the demo space running locally.

## Propose a reusable Base Demo component

If a custom component would be useful beyond one prospect demo, do not add it
directly without alignment. Open a GitHub issue first and discuss the use case
with the other SEs.

The issue should describe:

- the prospect or demo scenario it solves;
- the expected Storyblok component schema and fields;
- how content editors will use it;
- design-token, responsive, and Visual Editor requirements;
- whether it depends on external services or demo-space configuration.

After the approach is agreed, implement the component in this repository, add or
update the related Storyblok schema/configuration, test it locally with a demo
space, and open a pull request so it can become part of the shared Base Demo.

## Demo-Specific implementation notes

### Access token and path via URL parameters

We needed one deployed environment that could be used to display a large number of demo spaces that are generated on the fly. Therefore, the access tokens of these spaces are passed via URL parameters. In a more typical scenario, you would probably want to manage the access token as an environment variable. See the note in `nuxt.config.ts` and delete `app/plugins/storyblok.js` to remove the extra functionality for tokens as URL parameters altogether.

### Internationalization and language detection

For the demo, it has to be possible for any language to be added to the internationalization settings in Storyblok and detected automatically on the front end. All currently active language codes are retrieved from the Storyblok space to ensure this. When fetching a particular story based on the current route, it is checked whether any of the currently active language codes matches the first part of the route. For example, if the current route was `https://localhost:3000/de/home` and German had been added as a language, `de` would get added as the language parameter in the API request for the home story. You can look at the [getLanguage composable](app/composables/getLanguage.js) to see how it works. In a real-world project, you would usually know which languages are used on the website, allowing you to choose a simpler approach.

### Setting a real path for stories

The main drawback of handling internationalization as described above is that field-level translation will not work when setting a real path for certain stories (e.g., `/` instead of `home`). When setting a real path, the language code is no longer part of the route, thus making it impossible to detect.
