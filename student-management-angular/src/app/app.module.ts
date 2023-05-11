import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { StudentListComponent } from './student-list/student-list.component';
import { FacultyComponent } from './faculty/faculty.component';
import { HttpClientModule} from "@angular/common/http";

// Import the module from the SDK
import {AuthModule} from '@auth0/auth0-angular';
import { HeaderComponent } from './header/header.component';
import { AuthButtonComponent } from './auth-button/auth-button.component';
import { StudentProfileComponent } from './student-profile/student-profile.component';
import {NgOptimizedImage} from "@angular/common";

@NgModule({
  declarations: [
    AppComponent,
    StudentListComponent,
    FacultyComponent,
    HeaderComponent,
    AuthButtonComponent,
    StudentProfileComponent
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
      }
    }),
    NgOptimizedImage,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
