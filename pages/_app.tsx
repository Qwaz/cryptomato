import "semantic-ui-css/semantic.min.css";

import { AppProps } from "next/app";
import { SWRConfig } from "swr";
import fetch from "../lib/fetchJson";

// This default export is required in a new `pages/_app.js` file.
function MyApp({ Component, pageProps }: AppProps) {
  return (
    <SWRConfig
      value={{
        fetcher: fetch,
        onError: (err) => {
          console.error(err);
        },
      }}
    >
      <Component {...pageProps} />
    </SWRConfig>
  );
}

export default MyApp;
