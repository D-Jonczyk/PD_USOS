import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { StudentListComponent } from './student-list/student-list.component';
import { FacultyComponent } from './faculty/faculty.component';
import { HttpClientModule} from "@angular/common/http";
import { FormsModule} from "@angular/forms";

// Import the module from the SDK
import {AuthModule} from '@auth0/auth0-angular';
import { HeaderComponent } from './header/header.component';
import { AuthButtonComponent } from './auth-button/auth-button.component';
import { StudentProfileComponent } from './student-profile/student-profile.component';
import {NgOptimizedImage} from "@angular/common";
import {NgbModule} from "@ng-bootstrap/ng-bootstrap";
import { SidebarComponent } from './sidebar/sidebar.component';
import { RolesComponent } from './roles/roles.component';
import { EnrollmentsComponent } from './enrollments/enrollments.component';
import {ReactiveFormsModule} from "@angular/forms";
import { CoursesComponent } from './courses/courses.component';
import { AdminPanelComponent } from './admin-panel/admin-panel.component';
import { TeacherPanelComponent } from './teacher-panel/teacher-panel.component';
import {NewsComponent} from "./news/news.component";

@NgModule({
  declarations: [
    AppComponent,
    StudentListComponent,
    FacultyComponent,
    HeaderComponent,
    AuthButtonComponent,
    StudentProfileComponent,
    SidebarComponent,
    RolesComponent,
    EnrollmentsComponent,
    CoursesComponent,
    AdminPanelComponent,
    TeacherPanelComponent,
    NewsComponent
  ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,

        // Import the module into the application, with configuration
        AuthModule.forRoot({
            domain: 'dev-gybtlqrqithbjmgz.us.auth0.com',
            clientId: 'YpRo7KJC5yLf3K18bBRk7cyNo5zvqDMC',
            cacheLocation: 'localstorage',
            authorizationParams: {
                redirect_uri: window.location.origin
            },
        }),
        NgOptimizedImage,
        NgbModule,
        ReactiveFormsModule,
        FormsModule
    ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
