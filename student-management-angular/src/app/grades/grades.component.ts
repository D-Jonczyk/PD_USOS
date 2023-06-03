import {Component, OnInit} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AuthService} from "@auth0/auth0-angular";

@Component({
  selector: 'app-grades',
  templateUrl: './grades.component.html',
  styleUrls: ['./grades.component.scss']
})
export class GradesComponent {
  public response: any = null;
  public error: string | null = null;

  constructor(public auth: AuthService, private http: HttpClient) {
    this.auth.getAccessTokenSilently().subscribe(
      token => {
        console.log("token: ", token);
        this.http.get('http://localhost:8000/api/hello', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }).subscribe(
          response => {
            this.response = response;
            console.log("response: ", response)
            this.error = null;
          },
          err => {
            this.error = 'User not authenticated';
            this.response = null;
          }
        );
      },
      err => {
        this.error = 'User not authenticated';
        this.response = null;
      }
    );
  }

}
