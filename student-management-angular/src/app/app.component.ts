import { Component } from '@angular/core';
import {Router} from "@angular/router";
import { AuthService} from "@auth0/auth0-angular";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'student-management-angular';
  isAuthenticated: boolean = false;

  constructor(private router: Router, public auth: AuthService) {
    this.auth.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isAuthenticated = isAuthenticated;
    });
  }

  goToStudentList() {
    this.router.navigate(['/students']);
  }
}
