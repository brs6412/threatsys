import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface IOC {
  id: string;
  type_id: number;
  value: string;
  value_hash: string;
  tlp_level: string;
  active: boolean;
  metadata: Record<string, any>;
  source_org_id: string;
  created_by: string;
}

export interface User {
  id: string | null;
  first_name: string;
  last_name: string;
  email: string;
  organization: string | null;
  role: string;
  created_at: string | null;
  last_login: string | null;
}

@Injectable({
  providedIn: 'root'
})
export class Api {
  constructor(private http: HttpClient) { }
  getHomepage(): Observable<any> {
    return this.http.get(`${environment.apiUrl}/`)
  }
  getIocs(skip: number = 0, limit: number = 100): Observable<IOC[]> {
    return this.http.get<IOC[]>(`${environment.apiUrl}/iocs/`);
  }
  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${environment.apiUrl}/users/`);
  }
}
