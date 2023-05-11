import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {StudentListComponent} from "./student-list/student-list.component";
import {FacultyComponent} from "./faculty/faculty.component";
import {StudentProfileComponent} from "./student-profile/student-profile.component";


const routes: Routes = [
  { path: 'students', component: StudentListComponent },
  { path: 'faculty', component: FacultyComponent},
  { path: 'student-profile', component: StudentProfileComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
