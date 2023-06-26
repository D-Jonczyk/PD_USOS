import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DepartmentService {
  private url = 'http://localhost:8000/api/departments';

  constructor(private http: HttpClient) { }

  getDepartments(): Observable<any> {
    return this.http.get(this.url);
  }
}
