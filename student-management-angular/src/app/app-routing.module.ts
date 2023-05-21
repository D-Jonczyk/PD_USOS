import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {StudentListComponent} from "./student-list/student-list.component";
import {FacultyComponent} from "./faculty/faculty.component";
import {StudentProfileComponent} from "./student-profile/student-profile.component";
import {RolesComponent} from "./roles/roles.component";
import {EnrollmentsComponent} from "./enrollments/enrollments.component";


const routes: Routes = [
  { path: 'students', component: StudentListComponent },
  { path: 'faculty', component: FacultyComponent},
  { path: 'student-profile', component: StudentProfileComponent},
  { path: 'roles', component: RolesComponent},
  { path: 'enrollments', component: EnrollmentsComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
