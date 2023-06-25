import {Component, OnInit} from '@angular/core';
import {Router} from "@angular/router";
import { AuthService} from "@auth0/auth0-angular";
import {StudentService} from "./services/student.service";
import {HttpClient} from "@angular/common/http";
import { Student } from "./models/models";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'student-management-angular';
  isAuthenticated: boolean = false;

  constructor(private router: Router, public auth: AuthService, private studentService: StudentService,
              private http: HttpClient) {
    this.auth.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isAuthenticated = isAuthenticated;
    });
  }

  ngOnInit(): void {  }

}
