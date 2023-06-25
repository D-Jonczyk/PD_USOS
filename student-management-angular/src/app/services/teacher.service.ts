import {Injectable} from "@angular/core";
import {HttpClient} from "@angular/common/http";
import {AuthService} from "@auth0/auth0-angular";
import {Observable, switchMap} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class TeacherService {

  constructor(private http: HttpClient, private auth: AuthService) { }

  getTeacherCourses(): Observable<any> {
    return this.auth.idTokenClaims$.pipe(
      switchMap((claims: any) =>
        this.http.get<any>('http://localhost:8000/api/teacher/courses', {
          headers: {
            Authorization: `Bearer ${claims.__raw}`
          }
        })
      )
    );
  }

  updateStudentGrade(courseId: string, studentId: string, grade: string): Observable<any> {
    return this.auth.idTokenClaims$.pipe(
      switchMap((claims: any) =>
        this.http.put<any>(`http://localhost:8000/api/teacher/course/${courseId}/student/${studentId}/grade`, { grade }, {
          headers: {
            Authorization: `Bearer ${claims.__raw}`
          }
        })
      )
    );
  }

}
