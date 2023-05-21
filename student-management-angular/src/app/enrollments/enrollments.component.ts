import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { AuthService } from '@auth0/auth0-angular';

@Component({
  selector: 'app-enrollments',
  templateUrl: './enrollments.component.html',
  styleUrls: ['./enrollments.component.scss']
})
export class EnrollmentsComponent implements OnInit {
  enrollments: any[] = [];

  constructor(private http: HttpClient, private auth: AuthService) {}

  ngOnInit(): void {
    this.auth.user$.subscribe((user) => {
      if (user) {
        const userId = 1;

        this.http.get<any[]>(`http://localhost:8000/api/enrollments/${userId}`).subscribe(
          (enrollments) => {
            this.enrollments = enrollments;
          },
          (error) => {
            console.error('Failed to fetch enrollments:', error);
          }
        );
      }
    });
  }
}
