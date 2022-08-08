<!--HOSTED_DOCS_ONLY
import useBaseUrl from '@docusaurus/useBaseUrl';

export const Logo = (props) => {
  return (
    <div style={{ display: "flex", justifyContent: "center", padding: "20px" }}>
      <img
        height="150"
        alt="CI&T"
        src={useBaseUrl("https://ciandt.com/themes/custom/ciandt_theme/logo.svg")}
        {...props}
      />
    </div>
  );
};

<Logo />

<!--
HOSTED_DOCS_ONLY-->
<p align="center">
<img alt="DataHub" src="https://ciandt.com/themes/custom/ciandt_theme/logo.svg" height="150" />
</p>
<!-- -->

# CI&T DataHub: The Metadata Platform for the Modern Data Stack
[![Version](https://img.shields.io/github/v/release/datahub-project/datahub?include_prereleases)](https://github.com/datahub-project/datahub/releases/latest)

[![Follow](https://img.shields.io/twitter/follow/ciandt?label=Follow&style=social)](https://twitter.com/ciandt)
### 🏠 CI&T Homepage: [CI&T](https://ciandt.com/br/pt-br)

## For demonstration purpose, access:
https://github.com/los-brabos/hackathon/blob/master/template/orion_mlops_template/readme.md

## Introduction

DataHub is an open-source metadata platform for the modern data stack. You should also visit [DataHub Architecture](docs/architecture/architecture.md) to get a better understanding of how DataHub is implemented.

## DataHub Quickstart Guide
### Deploying DataHub
To deploy a new instance of DataHub, perform the following steps.

Install docker, jq and docker-compose v1 (if using Linux). Make sure to allocate enough hardware resources for Docker engine. Tested & confirmed config: 2 CPUs, 8GB RAM, 2GB Swap area, and 10GB disk space.

Launch the Docker Engine from command line or the desktop app.

Install the DataHub CLI

a. Ensure you have Python 3.6+ installed & configured. (Check using python3 --version)

b. Run the following commands in your terminal

```
python3 -m pip install --upgrade pip wheel setuptools
python3 -m pip uninstall datahub acryl-datahub || true  # sanity check - ok if it fails
python3 -m pip install --upgrade acryl-datahub
datahub version
```

To deploy a DataHub instance locally, run the following CLI command from your terminal

```
datahub docker quickstart
```

This will deploy a DataHub instance using docker-compose.

Upon completion of this step, you should be able to navigate to the DataHub UI at http://localhost:9002 in your browser. You can sign in using datahub as both the username and password.

To ingest the sample metadata, run the following CLI command from your terminal

```
datahub docker ingest-sample-data
```

## License

[Apache License 2.0](./LICENSE).
