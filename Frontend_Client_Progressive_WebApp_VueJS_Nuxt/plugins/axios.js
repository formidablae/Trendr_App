import https from 'https';
import services from '~/lib/factories/services';

export default function({ app, $axios }, inject) {
	if (!$axios) {
		console.error('Please make sure $axios module is added');
	}
	else {
		$axios.defaults.httpsAgent = new https.Agent({ rejectUnauthorized: false });

		const srv = services($axios);
		inject('services', srv);
	}

	$axios.onError(async (error) => {
		if (error.response && error.response.status === 401) {
			await app.$auth.logout();
		}

		return Promise.reject(error);
	});
}
