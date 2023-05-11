import { Component } from '@angular/core';
import {Router} from "@angular/router";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'student-management-angular';

  constructor(private router: Router) {
  }

  goToStudentList() {
    this.router.navigate(['/students']);
  }
}
