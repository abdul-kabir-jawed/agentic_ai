# 🔐 MCP Authorization Mastery Guide

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin-bottom: 30px;">

## What is MCP Authorization?

**MCP Authorization** is OAuth 2.1-based security that enables MCP clients to access protected servers on behalf of users. It provides standardized discovery, dynamic registration, and token-based authentication while ensuring tokens are bound to specific resources.

> **Think of it like this:** A hotel key card system where guests (clients) get room keys (tokens) from the front desk (authorization server) to access their rooms (MCP servers). The key only works for your specific room, not others, and expires after checkout.

</div>

---

## 🤔 The Core Problem Authorization Solves

<div style="background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 5px solid #ffc107; margin: 20px 0;">

### Without Authorization (Chaos)

**Problems:**
- No user identity or permissions
- Anyone can access any MCP server
- No way to delegate access safely
- Can't scale to enterprise environments
- Tokens could be reused across services
- Manual client setup for every server

### With MCP Authorization (Order)

**Benefits:**
- User consent and identity verification
- Granular permissions (scopes)
- Tokens bound to specific MCP servers
- Dynamic client registration
- Standardized OAuth 2.1 security
- Automatic discovery of auth endpoints

**Result:** Secure, scalable, enterprise-ready MCP deployments with proper access control!

</div>

---

## 🗺️ The Complete Authorization Journey

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 5px solid #667eea;">

```
Stage 1: 🔍 PROTECTED RESOURCE DISCOVERY (RFC 9728)
        ↓
    "Where do I get authorized?"
    - Client tries accessing MCP server
    - Gets 401 with WWW-Authenticate header
    - Fetches /.well-known/oauth-protected-resource
    - Discovers Authorization Server URL
        ↓
Stage 2: 🏢 AUTHORIZATION SERVER DISCOVERY (RFC 8414)
        ↓
    "What can this auth server do?"
    - Query /.well-known/oauth-authorization-server
    - Learn authorization_endpoint
    - Learn token_endpoint
    - Learn registration_endpoint
    - Learn jwks_uri for token validation
        ↓
Stage 3: 📝 DYNAMIC CLIENT REGISTRATION (RFC 7591)
        ↓
    "Register me automatically"
    - Client POSTs metadata to registration_endpoint
    - Receives client_id and client_secret
    - No manual pre-configuration needed
        ↓
Stage 4: 🎫 AUTHORIZATION CODE FLOW (OAuth 2.1)
        ↓
    "Get user consent and tokens"
    - Redirect user to authorization_endpoint
    - User logs in and grants permissions
    - Receive authorization code
    - Exchange code for access token
        ↓
Stage 5: 🔒 PKCE PROTECTION (OAuth 2.1 Section 7.5.2)
        ↓
    "Prevent code interception"
    - Generate code_verifier (random secret)
    - Create code_challenge (SHA256 hash)
    - Include challenge in auth request
    - Prove ownership with verifier in token exchange
        ↓
Stage 6: ✅ TOKEN VALIDATION & USAGE
        ↓
    "Verify and use tokens securely"
    - Client includes token in Authorization header
    - Server validates signature with JWKS
    - Server checks audience (aud claim)
    - Server verifies expiration and issuer
```

**Critical Point:** Every stage builds on the previous one - this is a sequential process!

</div>

---

## 🔍 Stage 1: Protected Resource Discovery

<div style="background: #e3f2fd; padding: 25px; border-radius: 10px; border: 2px solid #2196f3; margin: 20px 0;">

### The Discovery Dance

**Step 1: Client Makes Unauthenticated Request**

```http
POST /mcp HTTP/1.1
Host: mcp.example.com
Content-Type: application/json

{"jsonrpc": "2.0", "method": "tools/list", "id": 1}
```

**Step 2: Server Returns 401 with Discovery Hint**

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer as_uri="https://auth.example.com"
```

**Key Insight:** The `as_uri` parameter tells the client where to start!

**Step 3: Client Fetches Resource Metadata**

```http
GET /.well-known/oauth-protected-resource HTTP/1.1
Host: mcp.example.com
```

**Step 4: Server Returns Resource Metadata**

```json
{
  "resource": "https://mcp.example.com",
  "authorization_servers": [
    "https://auth.example.com"
  ]
}
```

**What We Learned:** The location of the Authorization Server!

</div>

---

## 🏢 Stage 2: Authorization Server Discovery

<div style="background: #f3e5f5; padding: 25px; border-radius: 10px; border: 2px solid #9c27b0; margin: 20px 0;">

### Learning Server Capabilities

**Client Queries Metadata Endpoint**

```http
GET /.well-known/oauth-authorization-server HTTP/1.1
Host: auth.example.com
```

**Server Returns Complete Metadata**

```json
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "registration_endpoint": "https://auth.example.com/register",
  "jwks_uri": "https://auth.example.com/jwks.json",
  "response_types_supported": ["code"],
  "grant_types_supported": ["authorization_code", "client_credentials"],
  "token_endpoint_auth_methods_supported": ["client_secret_post"],
  "code_challenge_methods_supported": ["S256"],
  "scopes_supported": ["openid", "mcp:read", "mcp:write"]
}
```

**What We Learned:** Every endpoint needed for OAuth flow!

</div>

---

## 📝 Stage 3: Dynamic Client Registration

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #e8f5e9; padding: 25px; border-radius: 10px; border: 2px solid #4caf50;">

### Registration Request

```json
POST /register HTTP/1.1
Host: auth.example.com
Authorization: Bearer <initial_access_token>
Content-Type: application/json

{
  "client_name": "My MCP Client",
  "redirect_uris": [
    "http://localhost:8888/callback"
  ],
  "grant_types": [
    "authorization_code",
    "client_credentials"
  ],
  "response_types": ["code"],
  "scope": "openid mcp:read mcp:write",
  "token_endpoint_auth_method": 
    "client_secret_post"
}
```

**Why Dynamic?**
- No manual configuration
- AI agents auto-register
- Scales to 10M agents
- Works with any MCP server

</div>

<div style="background: #fff3cd; padding: 25px; border-radius: 10px; border: 2px solid #ffc107;">

### Registration Response

```json
{
  "client_id": 
    "cf285ac3-70a8-417d-9ec4",
  "client_secret": 
    "supersecret123...",
  "client_id_issued_at": 1234567890,
  "client_secret_expires_at": 0,
  "redirect_uris": [
    "http://localhost:8888/callback"
  ],
  "grant_types": [
    "authorization_code",
    "client_credentials"
  ],
  "scope": 
    "openid mcp:read mcp:write"
}
```

**What We Got:**
- Unique client_id
- Secret for authentication
- Confirmed capabilities
- Ready for OAuth flow

</div>

</div>

---

## 🎫 Stage 4: Authorization Code Flow

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 25px; border-radius: 15px; margin: 20px 0;">

### The User Consent Journey

**Step 1: Construct Authorization URL**

```python
# Client generates state for CSRF protection
state = secrets.token_urlsafe(32)

auth_url = (
    f"{authorization_endpoint}"
    f"?response_type=code"
    f"&client_id={client_id}"
    f"&redirect_uri={redirect_uri}"
    f"&scope=openid mcp:read mcp:write"
    f"&state={state}"
    f"&resource=https://mcp.example.com"  # REQUIRED by MCP!
)
```

**Step 2: User Authenticates and Consents**

```
Browser opens: https://auth.example.com/authorize?...
User logs in: username + password
User sees: "My MCP Client wants to access mcp.example.com"
User clicks: "Authorize"
```

**Step 3: Authorization Code Redirect**

```http
GET /callback?code=abc123&state=<original_state> HTTP/1.1
Host: localhost:8888
```

**Step 4: Exchange Code for Token**

```http
POST /token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=abc123
&client_id=cf285ac3-70a8-417d-9ec4
&client_secret=supersecret123...
&redirect_uri=http://localhost:8888/callback
&resource=https://mcp.example.com
```

**Step 5: Receive Access Token**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "refresh_abc123...",
  "scope": "openid mcp:read mcp:write"
}
```

</div>

---

## 🔒 Stage 5: PKCE Protection

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### What is PKCE?

**PKCE (Proof Key for Code Exchange)** prevents authorization code interception attacks. It's **MANDATORY** for MCP clients per the specification.

### How PKCE Works

**Step 1: Generate Random Secret (code_verifier)**

```python
import secrets
import hashlib
import base64

# 43-128 characters, URL-safe
code_verifier = base64.urlsafe_b64encode(
    secrets.token_bytes(32)
).decode('utf-8').rstrip('=')

# Result: "dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"
```

**Step 2: Create Hash (code_challenge)**

```python
# SHA256 hash of the verifier
code_challenge = base64.urlsafe_b64encode(
    hashlib.sha256(code_verifier.encode('utf-8')).digest()
).decode('utf-8').rstrip('=')

# Result: "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM"
```

**Step 3: Send Challenge in Authorization Request**

```http
GET /authorize
  ?response_type=code
  &client_id=abc123
  &code_challenge=E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM
  &code_challenge_method=S256
  &state=xyz
  &resource=https://mcp.example.com
```

**Step 4: Send Verifier in Token Exchange**

```http
POST /token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=returned_code
&code_verifier=dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk
&client_id=abc123
```

**Step 5: Server Verifies**

```python
# Server checks: SHA256(code_verifier) == stored code_challenge
assert hashlib.sha256(
    received_verifier.encode()
).digest() == stored_challenge

# If match → issue token
# If mismatch → reject request
```

### Why PKCE is Critical

**Without PKCE:** Attacker intercepts authorization code → exchanges for token → game over

**With PKCE:** Attacker intercepts code → can't prove ownership without code_verifier → attack fails

</div>

---

## 🎯 Stage 6: Resource Parameter (RFC 8707)

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 15px; margin: 20px 0;">

### Token Audience Binding

**The Problem:** Without resource parameter, tokens could be reused across services (security nightmare!)

**The Solution:** Explicitly bind tokens to specific MCP servers

### Resource Parameter Rules

**1. MUST Include in Authorization Request**

```
&resource=https%3A%2F%2Fmcp.example.com
```

**2. MUST Include in Token Request**

```
&resource=https://mcp.example.com
```

**3. Use Canonical URI Format**

**Valid Examples:**
- `https://mcp.example.com/mcp`
- `https://mcp.example.com`
- `https://mcp.example.com:8443`
- `https://mcp.example.com/server/mcp`

**Invalid Examples:**
- `mcp.example.com` (missing scheme)
- `https://mcp.example.com#fragment` (contains fragment)

### Token Validation

**Server MUST check audience claim:**

```python
# Token payload
{
  "iss": "https://auth.example.com",
  "aud": "https://mcp.example.com",  # MUST match server's URI!
  "sub": "user123",
  "exp": 1234567890,
  "scope": "mcp:read mcp:write"
}

# Server validates
if token.aud != "https://mcp.example.com":
    return 403  # Token not for this server!
```

**Why Critical:** Prevents confused deputy attacks and token misuse

</div>

---

## ✅ Token Validation & Usage

<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin: 30px 0;">

<div style="background: #e3f2fd; padding: 25px; border-radius: 10px;">

### Client Usage

**Include in Authorization Header**

```http
POST /mcp HTTP/1.1
Host: mcp.example.com
Authorization: Bearer eyJhbGciOiJSUzI1NiIs...
Content-Type: application/json

{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search"
  },
  "id": 2
}
```

**Never in Query String!**

```http
❌ GET /mcp?token=abc123
✅ Authorization: Bearer abc123
```

**Required on Every Request**

Even in same session, include token on every HTTP request.

</div>

<div style="background: #f3e5f5; padding: 25px; border-radius: 10px;">

### Server Validation

**Step 1: Fetch Public Keys (JWKS)**

```python
# Get from jwks_uri
jwks = requests.get(
    "https://auth.example.com/jwks.json"
).json()
```

**Step 2: Verify Signature**

```python
from jose import jwt

decoded = jwt.decode(
    token,
    jwks,
    algorithms=['RS256'],
    audience='https://mcp.example.com',
    issuer='https://auth.example.com'
)
```

**Step 3: Check Claims**

```python
# Expiration
if decoded['exp'] < time.time():
    return 401  # Token expired

# Audience
if decoded['aud'] != server_uri:
    return 403  # Wrong audience

# Scopes
if 'mcp:write' not in decoded['scope']:
    return 403  # Insufficient permissions
```

</div>

</div>

---

## 🚨 Error Handling Mastery

<div style="background: #fff3cd; padding: 25px; border-radius: 10px; border-left: 5px solid #ffc107; margin: 20px 0;">

### Standard OAuth Errors

**invalid_token (401 Unauthorized)**

```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer error="invalid_token",
  error_description="The access token expired"
```

**Client Action:** Discard token, re-authenticate

**insufficient_scope (403 Forbidden)**

```http
HTTP/1.1 403 Forbidden
WWW-Authenticate: Bearer error="insufficient_scope",
  error_description="Token lacks 'mcp:write' scope",
  scope="mcp:write"
```

**Client Action:** Request new token with required scopes

**invalid_request (400 Bad Request)**

```http
HTTP/1.1 400 Bad Request

{
  "error": "invalid_request",
  "error_description": "Missing required 'resource' parameter"
}
```

**Client Action:** Fix request and retry

### MCP-Specific Error Patterns

**Wrong Audience**

```python
if token.aud != expected_audience:
    return {
        "status": 403,
        "error": "invalid_token",
        "error_description": 
            "Token audience does not match server URI"
    }
```

**Token Passthrough Attempt**

```python
# Server MUST NOT forward client's token to upstream APIs
❌ requests.get(upstream_api, headers={"Authorization": client_token})
✅ requests.get(upstream_api, headers={"Authorization": new_token})
```

</div>

---

## 🔐 Client Credentials Flow (Machine-to-Machine)

<div style="background: #e8f5e9; padding: 25px; border-radius: 10px; border: 2px solid #4caf50; margin: 20px 0;">

### When to Use

**Perfect For:**
- Server-to-server communication
- Background jobs and agents
- No user interaction needed
- System-level permissions

**Token Request (No User Involved)**

```http
POST /token HTTP/1.1
Host: auth.example.com
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=system_client_abc
&client_secret=system_secret_xyz
&scope=mcp:read mcp:write
&resource=https://mcp.example.com
```

**Token Response**

```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "mcp:read mcp:write"
}
```

**Key Differences from Authorization Code:**
- No user login or consent
- No authorization code exchange
- No refresh tokens (just request new token)
- Client credentials authenticate the request

</div>

---

## 🛡️ Security Best Practices

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0;">

<div style="background: #e8f5e9; padding: 25px; border-radius: 10px;">

### ✅ MUST Do

**Transport Security:**
- Use HTTPS for all endpoints
- HTTPS for redirect URIs (except localhost)

**Token Storage:**
- Never log tokens
- Use secure storage (keychain)
- Never expose in URLs

**PKCE:**
- Always use PKCE (mandatory)
- Use S256 method (SHA256)
- Generate cryptographically random verifiers

**State Parameter:**
- Always include state
- Verify state on callback
- Use cryptographically random values

**Resource Parameter:**
- Include in auth request
- Include in token request
- Use canonical URI format

**Token Validation:**
- Verify signature with JWKS
- Check expiration
- Check issuer
- Check audience (critical!)

</div>

<div style="background: #ffebee; padding: 25px; border-radius: 10px;">

### ❌ NEVER Do

**Token Misuse:**
- Never pass tokens in query strings
- Never log access tokens
- Never reuse tokens across services
- Never accept tokens without validation

**Token Passthrough:**
- Never forward client tokens to upstream APIs
- Never skip audience validation
- Never trust tokens without verification

**Registration:**
- Never hardcode client secrets in code
- Never skip redirect URI validation
- Never allow wildcard redirect URIs

**Discovery:**
- Never skip WWW-Authenticate parsing
- Never cache metadata forever
- Never ignore 401 responses

**PKCE:**
- Never skip PKCE (it's mandatory!)
- Never reuse code_verifier
- Never use plain method (only S256)

</div>

</div>

---

## 🧠 Mental Model

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; color: white; margin: 30px 0; text-align: center;">

### Authorization = Layered Security

**Layer 1: Discovery** 🔍  
Find out who's in charge of access control

**↓**

**Layer 2: Registration** 📝  
Get credentials to identify yourself

**↓**

**Layer 3: User Consent** 👤  
Prove the user approves your access

**↓**

**Layer 4: Token Acquisition** 🎫  
Receive proof of authorization

**↓**

**Layer 5: Token Validation** ✅  
Verify proof before granting access

**↓**

**Result:** Multi-layered defense preventing unauthorized access

</div>

---

## 🔑 Key Concepts Summary

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0;">

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 10px;">

### 🔍 Two-Stage Discovery
First find Authorization Server, then its capabilities

**Purpose:** Dynamic configuration without hardcoding

</div>

<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 25px; border-radius: 10px;">

### 📝 Dynamic Registration
Clients auto-register without manual setup

**Purpose:** Enable scalable AI agent deployment

</div>

<div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 25px; border-radius: 10px;">

### 🔒 PKCE Protection
Prevents authorization code interception

**Purpose:** Mandatory security for all MCP clients

</div>

<div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); color: white; padding: 25px; border-radius: 10px;">

### 🎯 Resource Parameter
Binds tokens to specific MCP servers

**Purpose:** Prevent token misuse and confused deputy attacks

</div>

</div>

---

## 🎯 Master It in One Sentence

<div style="background: linear-gradient(to right, #ffecd2 0%, #fcb69f 100%); padding: 40px; border-radius: 15px; margin: 30px 0; text-align: center; font-size: 1.2em; font-weight: bold;">

*"MCP Authorization uses OAuth 2.1 with mandatory PKCE and resource parameters to enable secure, discoverable, dynamically-registered client access to protected MCP servers, with tokens explicitly bound to specific resources through audience validation."*

</div>

---

## 📊 Complete Flow Diagram

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

```
┌─────────┐         ┌──────────────┐         ┌──────────────────┐
│ Client  │         │ MCP Server   │         │ Auth Server      │
└────┬────┘         └──────┬───────┘         └────────┬─────────┘
     │                     │                           │
     │ 1. Tools request    │                           │
     ├────────────────────►│                           │
     │ 2. 401 + WWW-Auth   │                           │
     │◄────────────────────┤                           │
     │                     │                           │
     │ 3. Get /.well-known/oauth-protected-resource   │
     ├────────────────────►│                           │
     │ 4. Resource metadata│                           │
     │◄────────────────────┤                           │
     │                     │                           │
     │ 5. Get /.well-known/oauth-authorization-server │
     ├────────────────────────────────────────────────►│
     │ 6. AS metadata      │                           │
     │◄────────────────────────────────────────────────┤
     │                     │                           │
     │ 7. POST /register   │                           │
     ├────────────────────────────────────────────────►│
     │ 8. client_id + secret                           │
     │◄────────────────────────────────────────────────┤
     │                     │                           │
     │ 9. Open browser with auth URL + PKCE + resource│
     ├────────────────────────────────────────────────►│
     │                     │    10. User login/consent │
     │                     │    11. Redirect with code │
     │◄────────────────────────────────────────────────┤
     │                     │                           │
     │ 12. Exchange code + code_verifier + resource    │
     ├────────────────────────────────────────────────►│
     │ 13. Access token    │                           │
     │◄────────────────────────────────────────────────┤
     │                     │                           │
     │ 14. Request + Bearer token                      │
     ├────────────────────►│                           │
     │                     │ 15. Validate token (JWKS) │
     │                     ├──────────────────────────►│
     │                     │ 16. Public keys           │
     │                     │◄──────────────────────────┤
     │ 17. Success response│                           │
     │◄────────────────────┤                           │
     │                     │                           │
```

**Key Points:**
- Steps 1-6: Discovery (find auth server and its capabilities)
- Steps 7-8: Registration (get client credentials)
- Steps 9-13: Authorization (user consent and token acquisition)
- Steps 14-17: Usage (protected API calls with validation)

</div>

---

## 💼 Real-World Implementation Examples

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Example 1: Python Client with PKCE

```python
import secrets
import hashlib
import base64
import requests
from urllib.parse import urlencode, parse_qs

class MCPOAuthClient:
    def __init__(self, mcp_server_url):
        self.mcp_server_url = mcp_server_url
        self.client_id = None
        self.client_secret = None
        self.access_token = None
        
    def discover_and_register(self):
        """Complete discovery and registration flow"""
        
        # Stage 1: Protected Resource Discovery
        response = requests.post(f"{self.mcp_server_url}/mcp")
        assert response.status_code == 401
        
        # Parse WWW-Authenticate header
        www_auth = response.headers['WWW-Authenticate']
        # Extract as_uri or fetch metadata directly
        
        metadata_url = f"{self.mcp_server_url}/.well-known/oauth-protected-resource"
        resource_metadata = requests.get(metadata_url).json()
        auth_server = resource_metadata['authorization_servers'][0]
        
        # Stage 2: Authorization Server Discovery
        as_metadata_url = f"{auth_server}/.well-known/oauth-authorization-server"
        self.as_metadata = requests.get(as_metadata_url).json()
        
        # Stage 3: Dynamic Client Registration
        registration_data = {
            "client_name": "My MCP Client",
            "redirect_uris": ["http://localhost:8888/callback"],
            "grant_types": ["authorization_code"],
            "response_types": ["code"],
            "scope": "openid mcp:read mcp:write",
            "token_endpoint_auth_method": "client_secret_post"
        }
        
        reg_response = requests.post(
            self.as_metadata['registration_endpoint'],
            json=registration_data,
            headers={"Authorization": f"Bearer {INITIAL_ACCESS_TOKEN}"}
        ).json()
        
        self.client_id = reg_response['client_id']
        self.client_secret = reg_response['client_secret']
        
    def generate_pkce(self):
        """Generate PKCE parameters"""
        code_verifier = base64.urlsafe_b64encode(
            secrets.token_bytes(32)
        ).decode('utf-8').rstrip('=')
        
        code_challenge = base64.urlsafe_b64encode(
            hashlib.sha256(code_verifier.encode('utf-8')).digest()
        ).decode('utf-8').rstrip('=')
        
        return code_verifier, code_challenge
    
    def authorize(self):
        """Start authorization code flow with PKCE"""
        code_verifier, code_challenge = self.generate_pkce()
        state = secrets.token_urlsafe(32)
        
        # Build authorization URL
        auth_params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': 'http://localhost:8888/callback',
            'scope': 'openid mcp:read mcp:write',
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
            'resource': self.mcp_server_url  # CRITICAL!
        }
        
        auth_url = f"{self.as_metadata['authorization_endpoint']}?{urlencode(auth_params)}"
        
        # Open browser and wait for callback
        print(f"Opening browser: {auth_url}")
        # ... callback server logic ...
        
        return code_verifier, state
    
    def exchange_code(self, code, code_verifier):
        """Exchange authorization code for access token"""
        token_data = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': 'http://localhost:8888/callback',
            'code_verifier': code_verifier,
            'resource': self.mcp_server_url  # CRITICAL!
        }
        
        token_response = requests.post(
            self.as_metadata['token_endpoint'],
            data=token_data
        ).json()
        
        self.access_token = token_response['access_token']
        return self.access_token
    
    def call_mcp_tool(self, method, params):
        """Make authenticated MCP request"""
        response = requests.post(
            f"{self.mcp_server_url}/mcp",
            json={
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": 1
            },
            headers={
                "Authorization": f"Bearer {self.access_token}"
            }
        )
        
        if response.status_code == 401:
            # Token expired, need to refresh
            raise TokenExpiredError()
        
        return response.json()

# Usage
client = MCPOAuthClient("https://mcp.example.com")
client.discover_and_register()
client.authorize()
# ... handle callback ...
client.call_mcp_tool("tools/list", {})
```

</div>

---

## 🔐 Server Token Validation Example

<div style="background: #1e1e1e; color: #d4d4d4; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Complete Token Validation

```python
from fastapi import FastAPI, HTTPException, Depends, Header
from jose import jwt, JWTError
import requests
from functools import lru_cache
import time

app = FastAPI()

SERVER_URI = "https://mcp.example.com"
AUTH_SERVER = "https://auth.example.com"

@lru_cache(maxsize=1)
def get_jwks():
    """Fetch and cache JWKS from authorization server"""
    metadata = requests.get(
        f"{AUTH_SERVER}/.well-known/oauth-authorization-server"
    ).json()
    
    jwks = requests.get(metadata['jwks_uri']).json()
    return jwks

def validate_token(authorization: str = Header(None)):
    """Validate Bearer token"""
    
    # Check Authorization header present
    if not authorization:
        raise HTTPException(
            status_code=401,
            headers={
                "WWW-Authenticate": 'Bearer error="invalid_token", '
                'error_description="Missing Authorization header"'
            }
        )
    
    # Check Bearer scheme
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        raise HTTPException(
            status_code=401,
            headers={
                "WWW-Authenticate": 'Bearer error="invalid_token", '
                'error_description="Invalid Authorization header format"'
            }
        )
    
    token = parts[1]
    
    try:
        # Decode and validate JWT
        jwks = get_jwks()
        
        payload = jwt.decode(
            token,
            jwks,
            algorithms=['RS256'],
            audience=SERVER_URI,  # CRITICAL: Check audience!
            issuer=AUTH_SERVER,
            options={
                'verify_signature': True,
                'verify_exp': True,
                'verify_aud': True,
                'verify_iss': True
            }
        )
        
        # Additional checks
        if payload.get('exp', 0) < time.time():
            raise HTTPException(
                status_code=401,
                headers={
                    "WWW-Authenticate": 'Bearer error="invalid_token", '
                    'error_description="Token has expired"'
                }
            )
        
        # Check audience explicitly (double-check)
        if SERVER_URI not in payload.get('aud', []):
            raise HTTPException(
                status_code=403,
                headers={
                    "WWW-Authenticate": 'Bearer error="invalid_token", '
                    f'error_description="Token audience mismatch. '
                    f'Expected {SERVER_URI}"'
                }
            )
        
        return payload
        
    except JWTError as e:
        raise HTTPException(
            status_code=401,
            headers={
                "WWW-Authenticate": f'Bearer error="invalid_token", '
                f'error_description="{str(e)}"'
            }
        )

@app.post("/mcp")
async def mcp_endpoint(token_data: dict = Depends(validate_token)):
    """Protected MCP endpoint"""
    
    # Check scopes for specific operations
    scopes = token_data.get('scope', '').split()
    
    if 'mcp:write' not in scopes:
        raise HTTPException(
            status_code=403,
            headers={
                "WWW-Authenticate": 'Bearer error="insufficient_scope", '
                'error_description="Operation requires mcp:write scope", '
                'scope="mcp:write"'
            }
        )
    
    # Process request with validated token
    return {"result": "success", "user": token_data.get('sub')}

@app.get("/.well-known/oauth-protected-resource")
async def protected_resource_metadata():
    """Protected Resource Metadata endpoint"""
    return {
        "resource": SERVER_URI,
        "authorization_servers": [AUTH_SERVER]
    }
```

</div>

---

## 🚀 Quick Reference Checklist

<div style="background: #f8f9fa; padding: 25px; border-radius: 10px; margin: 20px 0;">

### Client Implementation Checklist

- [ ] Parse WWW-Authenticate headers from 401 responses
- [ ] Fetch Protected Resource metadata (/.well-known/oauth-protected-resource)
- [ ] Fetch Authorization Server metadata (/.well-known/oauth-authorization-server)
- [ ] Implement dynamic client registration (RFC 7591)
- [ ] Generate PKCE parameters (code_verifier, code_challenge)
- [ ] Include resource parameter in all auth/token requests
- [ ] Generate cryptographically random state parameter
- [ ] Implement local callback server for redirect URI
- [ ] Exchange authorization code for access token
- [ ] Store tokens securely (never in plaintext)
- [ ] Include Bearer token in Authorization header
- [ ] Handle token expiration and refresh
- [ ] Implement proper error handling

### Server Implementation Checklist

- [ ] Implement /.well-known/oauth-protected-resource endpoint
- [ ] Return 401 with WWW-Authenticate header for unauth requests
- [ ] Validate Bearer tokens on every request
- [ ] Fetch and cache JWKS from authorization server
- [ ] Verify token signature using public keys
- [ ] Validate token expiration (exp claim)
- [ ] Validate token issuer (iss claim)
- [ ] Validate token audience (aud claim matches server URI)
- [ ] Check required scopes for operations
- [ ] Return appropriate HTTP status codes (401, 403, 400)
- [ ] Never pass through tokens to upstream APIs
- [ ] Use HTTPS in production

</div>

---

## 📚 Standards Reference

<div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0;">

<div style="background: #e3f2fd; padding: 20px; border-radius: 10px;">

### Core OAuth Specifications

**OAuth 2.1 (Draft)**
- Main authorization framework
- Mandatory PKCE requirement
- Security best practices

**RFC 8414**
- Authorization Server Metadata
- /.well-known/oauth-authorization-server
- Endpoint discovery

**RFC 7591**
- Dynamic Client Registration
- Automatic client provisioning
- No manual setup needed

</div>

<div style="background: #f3e5f5; padding: 20px; border-radius: 10px;">

### MCP-Specific Standards

**RFC 9728**
- Protected Resource Metadata
- /.well-known/oauth-protected-resource
- Authorization server location

**RFC 8707**
- Resource Indicators
- Token audience binding
- Prevents token misuse

**RFC 6750**
- Bearer Token Usage
- Authorization header format
- Error responses

</div>

</div>

---

<div style="text-align: center; margin-top: 50px; color: #6c757d; font-style: italic;">

**You now understand the complete MCP OAuth 2.1 authorization flow and can implement secure, enterprise-ready MCP servers and clients.**  
Build protected MCP systems with confidence! 🚀

</div>
