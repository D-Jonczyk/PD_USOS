import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable, switchMap} from "rxjs";
import {AuthService} from "@auth0/auth0-angular";

@Injectable({
  providedIn: 'root',
})
export class CourseService {
  private url = 'http://localhost:8000/api/courses'; // your API URL here

  constructor(private http: HttpClient, public auth: AuthService) {}

  getCourses(): Observable<any> {
      return this.auth.idTokenClaims$.pipe(
        switchMap((claims: any) =>
          this.http.get<any>('http://localhost:8000/api/courses', {
            headers: {
              Authorization: `Bearer ${claims.__raw}`
            }
          })
        )
      );
  }

  createCourse(course: {name: string; description: string; department: string, instructor: string }) {
    return this.auth.idTokenClaims$.pipe(
      switchMap((claims: any) =>
        this.http.post('http://localhost:8000/api/courses', course, {
          headers: {
            Authorization: `Bearer ${claims.__raw}`
          }
        })
      )
    );
  }

  getCourse(id: number) {
    return this.http.get(`${this.url}/${id}`);
  }

  updateCourse(id: number, course: any) {
    return this.http.put(`${this.url}/${id}`, course);
  }

  deleteCourse(id: number) {
    return this.http.delete(`${this.url}/${id}`);
  }
}
