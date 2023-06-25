import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {Observable, switchMap} from "rxjs";
import {AuthService} from "@auth0/auth0-angular";

@Injectable({
  providedIn: 'root'
})
export class AdminService {
  private apiUrl = 'http://localhost:8000/api';  // Update with your actual backend URL

  constructor(private http: HttpClient, private auth: AuthService) { }

  addDepartment(department: any): Observable<any> {
    return this.auth.idTokenClaims$.pipe(
      switchMap((claims: any) =>
        this.http.post(`${this.apiUrl}/departments`, department, {
          headers: {
            Authorization: `Bearer ${claims.__raw}`
          }
        })
      )
    );
  }

  addTeacher(teacher: any): Observable<any> {
    return this.auth.idTokenClaims$.pipe(
      switchMap((claims: any) =>
        this.http.post(`${this.apiUrl}/teachers`, teacher, {
          headers: {
            Authorization: `Bearer ${claims.__raw}`
          }
        })
      )
    );
  }
  // Add more methods as needed for other CRUD operations
}
