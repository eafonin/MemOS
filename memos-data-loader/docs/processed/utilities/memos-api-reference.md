# MemOS REST API Reference

**Source:** https://memos-docs.openmem.net/docs/api/info
**Scraped:** 2025-10-16
**Type:** Official Documentation - API Reference

---

## Core Endpoints

**Base Path:** `/api`
**Content-Type:** `application/json`

---

## Configuration

### POST /configure
Set MemOS system configuration including LLM, memory reader, scheduler, and user manager settings

---

## User Management

### GET /users
List all active users

**Response:**
```json
{
  "code": 200,
  "message": "Success",
  "data": {
    "users": [...]
  }
}
```

### POST /users
Create new user

**Request Body:**
```json
{
  "user_id": "string",
  "user_name": "string",
  "role": "string"
}
```

**Required Parameters:**
- `user_id` - User identifier (string, required)
- `user_name` - Display name (string, required)
- `role` - User role (string, required)

### GET /users/me
Retrieve current user information and accessible cubes

---

## Memory Cube Operations

### POST /mem_cubes
Register new MemCube

**Request Body:**
```json
{
  "name": "string",
  "path": "string",
  "mem_cube_id": "string (optional)"
}
```

**Description:** Register a new MemCube with name/path and optional ID

### DELETE /mem_cubes/{mem_cube_id}
Unregister a MemCube

**Path Parameters:**
- `mem_cube_id` - Memory cube identifier (string, required)

### POST /mem_cubes/{cube_id}/share
Share cube with another user

**Path Parameters:**
- `cube_id` - Memory cube identifier (string, required)

**Request Body:**
```json
{
  "target_user_id": "string"
}
```

---

## Memory Management

### POST /memories
Store new memories in a MemCube

**Request Body Options:**

**Option 1: Message-based**
```json
{
  "user_id": "string",
  "messages": [
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "mem_cube_id": "string"
}
```

**Option 2: Direct content**
```json
{
  "user_id": "string",
  "memory_content": "string",
  "mem_cube_id": "string"
}
```

**Option 3: Document import**
```json
{
  "user_id": "string",
  "doc_path": "string",
  "mem_cube_id": "string"
}
```

### GET /memories
Retrieve all memories from a MemCube

**Query Parameters:**
- `mem_cube_id` - Memory cube identifier (string, required)
- `user_id` - User identifier (string, required)

### GET /memories/{mem_cube_id}/{memory_id}
Fetch specific memory

**Path Parameters:**
- `mem_cube_id` - Memory cube identifier (string, required)
- `memory_id` - Specific memory identifier (string, required)

### PUT /memories/{mem_cube_id}/{memory_id}
Update existing memory

**Path Parameters:**
- `mem_cube_id` - Memory cube identifier (string, required)
- `memory_id` - Specific memory identifier (string, required)

**Request Body:**
```json
{
  "memory_content": "string"
}
```

### DELETE /memories/{mem_cube_id}/{memory_id}
Remove specific memory

**Path Parameters:**
- `mem_cube_id` - Memory cube identifier (string, required)
- `memory_id` - Specific memory identifier (string, required)

### DELETE /memories/{mem_cube_id}
Delete all memories from cube

**Path Parameters:**
- `mem_cube_id` - Memory cube identifier (string, required)

---

## Search & Chat

### POST /search
Search for memories across MemCubes

**Request Body:**
```json
{
  "user_id": "string",
  "query": "string",
  "install_cube_ids": ["string"],
  "limit": "number (optional)"
}
```

**Parameters:**
- `user_id` - User identifier (string, required)
- `query` - Search query (string, required)
- `install_cube_ids` - Array of cube IDs to search (array, optional)
- `limit` - Maximum results (number, optional)

### POST /chat
Chat with the MemOS system

**Request Body:**
```json
{
  "user_id": "string",
  "message": "string",
  "install_cube_ids": ["string"]
}
```

---

## Response Structure

**Success Response:**
```json
{
  "code": 200,
  "message": "Operation successful",
  "data": {
    // Response data varies by endpoint
  }
}
```

**Error Response:**
```json
{
  "code": 4xx/5xx,
  "message": "Error description",
  "data": null
}
```

---

## Authentication

**Method:** Token-based or Bearer token
**Header Format:**
- `Authorization: Token YOUR_API_KEY` (cloud service)
- `Authorization: Bearer YOUR_TOKEN` (playground likely)

---

## Three Primary Data Loading Methods Identified

### 1. Message-Based Import (Chat Sessions)
**Endpoint:** `POST /memories`
**Format:**
```json
{
  "user_id": "string",
  "messages": [{"role": "...", "content": "..."}],
  "mem_cube_id": "string"
}
```
**Use Case:** Import conversation logs, chat sessions

### 2. Direct Content Import (CLI Stdout)
**Endpoint:** `POST /memories`
**Format:**
```json
{
  "user_id": "string",
  "memory_content": "string",
  "mem_cube_id": "string"
}
```
**Use Case:** Import CLI tool outputs, logs, text content

### 3. Document Import (File-Based)
**Endpoint:** `POST /memories`
**Format:**
```json
{
  "user_id": "string",
  "doc_path": "string",
  "mem_cube_id": "string"
}
```
**Use Case:** Import documents, files, structured data

---

## Critical Implementation Notes

1. **All operations require user_id** - user must exist before data import
2. **MemCube required** - must register cube before storing memories
3. **Three distinct import patterns** - messages, content, document
4. **Standardized response format** - consistent error handling needed
5. **Search supports multiple cubes** - flexible memory retrieval

---

## Next Steps for Data Loader

- [ ] Implement user creation/verification
- [ ] Implement MemCube registration
- [ ] Support all three import patterns
- [ ] Handle authentication with Bearer token
- [ ] Implement error handling for API responses
