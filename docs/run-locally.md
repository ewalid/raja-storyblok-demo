# Run Locally

Use these steps when you need to run this frontend against a Storyblok demo
space from your local machine.

## Basic Setup

1. Clone the repository and install dependencies:

```bash
npm install
```

2. Create an `.env` file with your preview access token. You can find it in your
   Storyblok space under `Settings > Access Tokens`.

```bash
STORYBLOK_TOKEN=your-preview-access-token
```

3. Run the development server:

```bash
npm run dev
```

## HTTPS Setup

Use HTTPS when you want to run the frontend inside the Storyblok Visual Editor.

1. Install `mkcert` if you do not have it already:

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

- `localhost.pem` certificate;
- `localhost-key.pem` private key.

4. Run the development server with HTTPS:

```bash
npm run devs
```

The HTTPS configuration is set up in `nuxt.config.ts` using the generated
certificate files. The server will be available at `https://localhost:3000`.

> If you use Bun or another runtime/package manager, replace `npm` with the
> matching command, for example `bun install` and `bun run devs`.

## Connect Storyblok Visual Editor

In your Storyblok space, go to `Settings > Visual Editor > Location` or use
**Add Preview URLs**, then set:

```text
https://localhost:3000/?token=YOURSPACEPREVIEWTOKEN&path=
```

Replace `YOURSPACEPREVIEWTOKEN` with your space's Preview access token.

Next, go to `Settings > Maintenance Mode` and disable `Example Mode`. This makes
sure the preview URL you just configured is used in the Visual Editor.

Finally, open your **Home** story and see the demo space running locally.
