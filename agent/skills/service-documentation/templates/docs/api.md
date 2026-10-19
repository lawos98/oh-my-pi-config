# API references

An API reference is optional. This workflow ships no service specification and makes no claims about real endpoints. Keep this page as guidance until an owner supplies a reviewed contract.

## Establish the contract

Use an approved OpenAPI document generated from or maintained with the service. Record its owner, source revision, and generation procedure. Compare documented operations, parameters, responses, and security requirements with the implementation. Remove secrets, personal data, private server addresses, and unsafe examples before including the document in a site.

A static link to the reviewed specification is sufficient when a separate reference UI adds no value. This example remains in a code fence until the file exists:

```markdown
[Download the reviewed OpenAPI contract](assets/api/openapi.json)
```

## Optional same-origin reference

If the project already has a reviewed API renderer, publish its static entry page and dependencies under `docs/assets/api/`. Keep the specification and scripts on the same origin. Do not load a CDN renderer, use a proxy service, or install Scalar as part of this workflow.

A reviewed read-only reference can be linked or embedded:

```html
<p><a href="assets/api/index.html">Open the read-only API reference</a></p>
<iframe src="assets/api/index.html" title="Read-only API contract reference"
        width="100%" height="720" loading="lazy"
        sandbox="allow-scripts"></iframe>
```

This restrictive sandbox gives the document an opaque origin. Some renderers cannot fetch their same-origin specification in that mode. Prefer a direct link or a renderer that embeds the reviewed contract rather than weakening the sandbox without review. A direct link runs with the site's origin privileges, so review its HTML and scripts first.

## Secure configuration

Use the renderer's version-specific documentation to disable request execution, authentication inputs, proxy routing, remote specification loading, telemetry, and external assets. Do not assume that hiding a request button prevents network calls. Never embed tokens or production credentials in configuration or examples. An iframe sandbox does not prevent all network access and does not make a renderer read-only.

If those settings cannot be established and checked, publish the static contract link only. A hosting Content Security Policy can further limit scripts, connections, and frames, but it needs deployment-specific review. Do not claim this template installs such a policy.

When verification is authorized, inspect browser requests and exercise navigation and keyboard controls. Confirm that the reference loads only reviewed assets and cannot send API requests. Keep any interactive API testing in a separate, explicitly authorized environment.
