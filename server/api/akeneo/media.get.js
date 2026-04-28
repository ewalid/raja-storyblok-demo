import { getAkeneoAccessToken, invalidateAkeneoTokenCache } from '../../utils/akeneoToken';
import { isValidAkeneoMediaCode } from '../../utils/akeneoMediaCode';

export default defineEventHandler(async (event) => {
  const query = getQuery(event);
  const raw = query.code;
  const code = typeof raw === 'string' ? raw : Array.isArray(raw) ? raw[0] : '';

  if (!isValidAkeneoMediaCode(code)) {
    throw createError({ statusCode: 400, statusMessage: 'Invalid media code' });
  }

  const config = useRuntimeConfig();
  const akeneoConfig = config.akeneo;
  const baseUrl = String(akeneoConfig.baseUrl || '').replace(/\/$/, '');
  if (!baseUrl) {
    throw createError({ statusCode: 503, statusMessage: 'Akeneo is not configured' });
  }

  const pathEncoded = code.split('/').map(encodeURIComponent).join('/');
  const mediaUrl = `${baseUrl}/api/rest/v1/media-files/${pathEncoded}/download`;

  const fetchMedia = async bearer =>
    fetch(mediaUrl, {
      headers: { Authorization: `Bearer ${bearer}` },
    });

  let token = await getAkeneoAccessToken();
  let res = await fetchMedia(token);

  if (res.status === 401) {
    invalidateAkeneoTokenCache();
    token = await getAkeneoAccessToken({ forceRefresh: true });
    res = await fetchMedia(token);
  }

  if (!res.ok) {
    throw createError({
      statusCode: res.status === 404 ? 404 : 502,
      statusMessage: 'Akeneo media request failed',
    });
  }

  const contentType = res.headers.get('content-type') || 'application/octet-stream';
  setResponseHeader(event, 'Content-Type', contentType);
  setResponseHeader(event, 'Cache-Control', 'private, max-age=300');

  return new Uint8Array(await res.arrayBuffer());
});
