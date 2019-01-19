<!-- markdown-swagger -->
 Endpoint                             | Method | Auth? | Description                              
 ------------------------------------ | ------ | ----- | -----------------------------------------
 `/api/v1/admin/locks`                | POST   | No    | Creates a lock given an admin id token   
 `/api/v1/locks/{lock_id}/lockStatus` | GET    | No    | Gets the lock status of a user owned lock
 `/api/v1/locks/{lock_id}/lockStatus` | PUT    | No    | Updates a lock status                    
 `/api/v1/user`                       | GET    | No    | Returns user information                 
 `/api/v1/user`                       | POST   | No    | Returns user information                 
 `/api/v1/userLocks`                  | GET    | No    | Returns a list of locks owned by a user  
 `/api/v1/userLocks`                  | POST   | No    | Adds a valid lock id to a user's account 
<!-- /markdown-swagger -->
