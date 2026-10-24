# Stock asset and download approval
Maintain an asset manifest with ID, source URL, creator/provider, intended scene, destination verified, preview, license type, commercial use permitted, price if any, approval status, download status and local path.

States: PROPOSED -> APPROVED_BY_USER -> LICENSED_OR_AUTHORIZED -> DOWNLOADED -> USED.
Never change state without actual evidence. Distinguish free licensed assets from paid assets. Only download assets individually approved by the user where approval is required.
Respect Shutterstock and other providers' terms, authentication, seat limits and IP/security controls. Do not use proxies, remote routing or workarounds to conceal identity or evade restrictions. If a remote browser cannot download, ask user to download via their authorized session and supply file.
Approval request format: thumbnail/preview link | provider | ID | price | usage rights | scene | reason for selection.
