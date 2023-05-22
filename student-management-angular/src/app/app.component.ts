import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import { AuthService} from "@auth0/auth0-angular";
import {StudentService} from "./services/student.service";
import {HttpClient} from "@angular/common/http";
import { Student } from "./models/student.model";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'student-management-angular';
  isAuthenticated: boolean = false;
  studentData: any = {
    // Set the student data here, such as auth0_id, first_name, last_name, etc.
  };

  constructor(private router: Router, public auth: AuthService, private studentService: StudentService,
              private http: HttpClient) {
    this.auth.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isAuthenticated = isAuthenticated;
    });
  }

  ngOnInit(): void {
    this.auth.isAuthenticated$.subscribe((isAuthenticated) => {
      if (isAuthenticated) {
        // User is authenticated, call the checkStudentExistence function
        this.checkStudentExistence();
      }
    });
  }
 checkStudentExistence(): void {
    // Get the user's auth0_id from the Auth0 session
    this.auth.idTokenClaims$.subscribe((claims) => {
      const auth0_id = claims?.['sub'];

      if (auth0_id) {
        // Get the user object from the Auth0 session
        this.auth.user$.subscribe((student) => {
          const studentObject: {
            major: any;
            date_of_birth: any;
            last_name: any;
            gpa: any;
            auth0_id: any;
            first_name: string;
            email: string;
            username: string
          } = {
            first_name: student?.['name'] || '',
            last_name: student?.['last_name'] || 'N/A',
            email: student?.email || '',
            major: 'informatyka',
            date_of_birth: student?.['date_of_birth'] || student?.['updated_at'],
            username: student?.['nickname'] || '',
            gpa: 3.0,
            auth0_id: auth0_id,
            // Assign additional properties as needed
          };
            console.log('studentobject:', studentObject);
          // Make the HTTP POST request to the check_student endpoint
          this.http.post('http://localhost:8000/api/check_student', studentObject).subscribe(
            (response) => {
              // Student already exists or has been added successfully
              console.log(response);
            },
            (error) => {
              // Handle error response
              console.error('Failed to check student existence:', error);
            }
          );
        });
      }
    });
  }

}
