import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Api, User } from '../../services/api';

@Component({
  selector: 'app-users',
  imports: [CommonModule],
  templateUrl: './users.html',
  styleUrl: './users.scss'
})
export class Users {
  users: User[] = [];
  loading = true;
  error = '';

  constructor(private apiService: Api) { }

  ngOnInit(): void {
    this.apiService.getUsers().subscribe({
      next: (data) => {
        this.users = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load Users';
        console.error(err);
        this.loading = false;
      }
    })
  }
}
