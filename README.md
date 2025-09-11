# Storyblok Solution Engineers Demo

This frontend is used when you [create a new demo space (for **Solution Engineers**) in Storyblok](https://app.storyblok.com/#/me/spaces/new?tab=experience-demo). It is built using [Nuxt 3](https://v3.nuxtjs.org/) and [TailwindCSS](https://tailwindcss.com/).

> The repository is <https://github.com/storyblok/storyblok-demo-default-se> . It is a forked repository from the JoyFul Demo <https://github.com/storyblok/storyblok-demo-default-v2>

Feel free to explore and reuse the code, but please be aware of the [demo-specific implementation practices](#demo-specific-implementation-notes), which deviate from the most common implementation practices.

## Showcasing a Demo

You can easily showcase a demo by creating a new space at this URL: <https://app.storyblok.com/#/me/spaces/new?tab=experience-demo> and selecting the `Solutions Demo Environment`.

> If yuo want to customize the PReview URL you can use: <https://storyblok-demo-default-se.netlify.app/?token=YOURSPACEPREVIEWACCESSTOKEN&path=>. Yuo can replace `YOURSPACEPREVIEWACCESSTOKEN` with your Preview access token.

If you need to **customize/implement new components** for a specific demo, you can also run the project locally.

## Run locally

To run the demo locally (e.g., when adding or testing custom components), follow these steps:

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

If you have `mkcert` installed and you already have your `localhost.pem` files generated with the command `mkcert localhost` you can run:

```bash
npm run devs
```

> Note: if you want to use Bun or some other runtime/packagemanager you can replace `npm` with the proper command, for example `bun install` and `bun run devs`

In your Storyblok space, go to **Settings** > **Visual Editor** and set `https://localhost:3000/` as the default environment.

> Note: if you didn't set the access token in your localhost (for example you want to swtich your localhost code quickly across different spaces, you can set the access token -and the path- in the Preview URL: ``https://localhost:3000/?token=YOURSPACEPREVIEWTOKEN&path=`). Replace `YOURSPACEPREVIEWTOKEN` with your Space **Preview** access token.

Finally, open your **Home** story and see the demo space running locally. Happy building!

## Demo-Specific implementation notes

### Access token and path via URL parameters

We needed one deployed environment that could be used to display a large number of demo spaces that are generated on the fly. Therefore, the access tokens of these spaces are passed via URL parameters. In a more typical scenario, you would probably want to manage the access token as an environment variable. See the note in `nuxt.config.js` and delete `plugins/storyblok.js` to remove the extra functionality for tokens as URL parameters altogether.

### Internationalization and language detection

For the demo, it has to be possible for any language to be added to the internationalization settings in Storyblok and detected automatically on the front end. All currently active language codes are retrieved from the Storyblok space to ensure this. When fetching a particular story based on the current route, it is checked whether any of the currently active language codes matches the first part of the route. For example, if the current route was `https://localhost:3000/de/home` and German had been added as a language, `de` would get added as the language parameter in the API request for the home story. You can look at the [getLanguage composable](composables/getLanguage.js) to see how it works. In a real-world project, you would usually know which languages are used on the website, allowing you to choose a simpler approach.

### Setting a real path for stories

The main drawback of handling internationalization as described above is that field-level translation will not work when setting a real path for certain stories (e.g., `/` instead of `home`). When setting a real path, the language code is no longer part of the route, thus making it impossible to detect.
