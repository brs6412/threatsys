import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

export interface IOCTypeResponse {
  id: number;
  name: string;
  category?: string;
}

export interface OrganizationResponse {
  id: string; // UUID as string
  name: string;
}

export interface OrganizationDetailResponse extends OrganizationResponse {
  created_at: string; // datetime as ISO string
  updated_at: string;
}

export interface RoleBase {
  id: number;
  name: string;
}

export interface UserResponse {
  id: string; // UUID as string
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  organization?: string;
  created_at: string; // datetime as ISO string
  last_login?: string; // datetime as ISO string
}

export interface UserDetailResponse {
  id: string; // UUID as string
  email: string;
  first_name: string;
  last_name: string;
  role: RoleBase;
  organization?: OrganizationResponse;
  created_at: string; // datetime as ISO string
  last_login?: string; // datetime as ISO string
}

export interface IOCResponse {
  id: string; // UUID as string
  value: string;
  value_hash: string;
  tlp_level: string;
  active: boolean;
  source_organization?: string;
  creator?: string;
  last_seen: string; // datetime as ISO string
  ioc_type: IOCTypeResponse;
}

export interface IOCDetailResponse {
  id: string; // UUID as string
  value: string;
  value_hash: string;
  tlp_level: string;
  metadata_?: { [key: string]: any }; // Dict type
  active: boolean;
  source_organization?: string;
  creator?: string;
  created_at: string; // datetime as ISO string
  updated_at: string; // datetime as ISO string
  last_seen: string; // datetime as ISO string
  received_at: string; // datetime as ISO string
  ioc_type: IOCTypeResponse;
}

// Create/Update interfaces (for POST/PUT requests)
export interface UserCreate {
  email: string;
  first_name: string;
  last_name: string;
  role?: string;
  organization?: string;
  password?: string; // Likely needed for creation
}

export interface UserUpdate {
  email?: string;
  first_name?: string;
  last_name?: string;
  role?: string;
  organization?: string;
}

export interface IOCCreate {
  value: string;
  tlp_level: string;
  active?: boolean;
  source_organization?: string;
  creator?: string;
  ioc_type_id: number; // Reference to IOCType
  metadata_?: { [key: string]: any };
}

export interface IOCUpdate {
  value?: string;
  tlp_level?: string;
  active?: boolean;
  source_organization?: string;
  creator?: string;
  ioc_type_id?: number;
  metadata_?: { [key: string]: any };
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:8000'; // Adjust to your FastAPI server URL

  private httpOptions = {
    headers: new HttpHeaders({
      'Content-Type': 'application/json'
    })
  };

  constructor(private http: HttpClient) { }

  // User endpoints
  getUsers(): Observable<UserResponse[]> {
    return this.http.get<UserResponse[]>(`${this.baseUrl}/users`)
      .pipe(catchError(this.handleError));
  }

  getUser(id: string): Observable<UserDetailResponse> {
    return this.http.get<UserDetailResponse>(`${this.baseUrl}/users/${id}`)
      .pipe(catchError(this.handleError));
  }

  createUser(user: UserCreate): Observable<UserResponse> {
    return this.http.post<UserResponse>(`${this.baseUrl}/users`, user, this.httpOptions)
      .pipe(catchError(this.handleError));
  }

  updateUser(id: string, user: UserUpdate): Observable<UserResponse> {
    return this.http.put<UserResponse>(`${this.baseUrl}/users/${id}`, user, this.httpOptions)
      .pipe(catchError(this.handleError));
  }

  deleteUser(id: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/users/${id}`)
      .pipe(catchError(this.handleError));
  }

  // IOC endpoints
  getIOCs(): Observable<IOCResponse[]> {
    return this.http.get<IOCResponse[]>(`${this.baseUrl}/iocs`)
      .pipe(catchError(this.handleError));
  }

  getIOC(id: string): Observable<IOCDetailResponse> {
    return this.http.get<IOCDetailResponse>(`${this.baseUrl}/iocs/${id}`)
      .pipe(catchError(this.handleError));
  }

  createIOC(ioc: IOCCreate): Observable<IOCResponse> {
    return this.http.post<IOCResponse>(`${this.baseUrl}/iocs`, ioc, this.httpOptions)
      .pipe(catchError(this.handleError));
  }

  updateIOC(id: string, ioc: IOCUpdate): Observable<IOCResponse> {
    return this.http.put<IOCResponse>(`${this.baseUrl}/iocs/${id}`, ioc, this.httpOptions)
      .pipe(catchError(this.handleError));
  }

  deleteIOC(id: string): Observable<any> {
    return this.http.delete(`${this.baseUrl}/iocs/${id}`)
      .pipe(catchError(this.handleError));
  }

  // IOC Types endpoint (you'll likely need this for the dropdowns)
  getIOCTypes(): Observable<IOCTypeResponse[]> {
    return this.http.get<IOCTypeResponse[]>(`${this.baseUrl}/ioc-types`)
      .pipe(catchError(this.handleError));
  }

  // Organizations endpoint (for user organization dropdown)
  getOrganizations(): Observable<OrganizationResponse[]> {
    return this.http.get<OrganizationResponse[]>(`${this.baseUrl}/organizations`)
      .pipe(catchError(this.handleError));
  }

  // Roles endpoint (for user role dropdown)
  getRoles(): Observable<RoleBase[]> {
    return this.http.get<RoleBase[]>(`${this.baseUrl}/roles`)
      .pipe(catchError(this.handleError));
  }

  private handleError(error: any) {
    console.error('API Error:', error);
    return throwError(() => error);
  }
}