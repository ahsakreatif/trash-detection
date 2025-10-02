import adapter from '@sveltejs/adapter-static';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

/** @type {import('@sveltejs/kit').Config} */
const config = {
	// Consult https://kit.svelte.dev/docs/integrations#preprocessors
	// for more information about preprocessors
	preprocess: vitePreprocess(),

	kit: {
		// adapter-static configured for SPA (client-side only)
		adapter: adapter({
			fallback: 'index.html' // SPA mode - all routes fallback to index.html
		}),
		paths: {
			base: '/pdp2024'
		}
	}
};

export default config;
