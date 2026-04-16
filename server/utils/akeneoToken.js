/** In-memory OAuth access token (server process only). */
let cache = { token: null, expiresAt: 0 };

export function invalidateAkeneoTokenCache() {
  cache = { token: null, expiresAt: 0 };
}

/**
 * Returns a valid Akeneo REST API Bearer token (password grant).
 * @param {{ forceRefresh?: boolean }} [options]
 */
export async function getAkeneoAccessToken(options = {}) {
  const { forceRefresh = false } = options;
  const config = useRuntimeConfig();
  const { baseUrl, clientId, clientSecret, username, password } = config.akeneo || {};

  if (!baseUrl || !clientId || !clientSecret || !username || !password) {
    throw createError({
      statusCode: 503,
      statusMessage: 'Akeneo is not configured',
    });
  }

  const skewMs = 60_000;
  if (!forceRefresh && cache.token && Date.now() < cache.expiresAt - skewMs) {
    return cache.token;
  }

  const tokenUrl = `${String(baseUrl).replace(/\/$/, '')}/api/oauth/v1/token`;
  const res = await fetch(tokenUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      grant_type: 'password',
      username,
      password,
      client_id: clientId,
      client_secret: clientSecret,
    }),
  });

  if (!res.ok) {
    throw createError({
      statusCode: 502,
      statusMessage: 'Akeneo authentication failed',
    });
  }

  const data = await res.json();
  if (!data.access_token) {
    throw createError({
      statusCode: 502,
      statusMessage: 'Akeneo token response invalid',
    });
  }

  const expiresInSec = Number(data.expires_in) || 3600;
  cache = {
    token: data.access_token,
    expiresAt: Date.now() + expiresInSec * 1000,
  };

  return cache.token;
}
