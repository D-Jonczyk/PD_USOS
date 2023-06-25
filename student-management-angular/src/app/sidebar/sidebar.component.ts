import {Component, OnInit} from '@angular/core';
import { AuthService} from "@auth0/auth0-angular";
import {map} from "rxjs/operators";
import {RoleService} from "../services/auth.service";

@Component({
  selector: 'app-sidebar',
  templateUrl: './sidebar.component.html',
  styleUrls: ['./sidebar.component.scss']
})
export class SidebarComponent implements OnInit {
  isAuthenticated: boolean = false;
  isAdmin: boolean = false;
  userRole: string | null = null;

  constructor(private auth: AuthService, private roleService: RoleService) {
      this.auth.isAuthenticated$.subscribe((isAuthenticated) => {
      this.isAuthenticated = isAuthenticated;
    });
  }
  ngOnInit(): void {
    this.auth.idTokenClaims$.subscribe((claims: any) => {
      this.userRole = claims['http://localhost:4200/roles'] || null;
      if(claims['is_admin']){
        this.isAdmin = claims['is_admin'];
      }
    });
  }
}
