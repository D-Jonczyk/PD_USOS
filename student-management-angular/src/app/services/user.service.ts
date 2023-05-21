import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private readonly REGISTER_URL = 'http://localhost:8000/register'; // Update with your Django backend URL

  constructor(private http: HttpClient) { }

  registerUser(username: string, email: string, departmentId: number): Observable<any> {
    const user = {
      username,
      email,
      department_id: departmentId
      // Add other user data fields as needed
    };

    return this.http.post(this.REGISTER_URL, user);
  }
}
