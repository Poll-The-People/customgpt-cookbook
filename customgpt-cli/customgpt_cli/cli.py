#!/usr/bin/env python3
"""
CustomGPT CLI - Command line interface for CustomGPT SDK.

This module provides a command-line interface for interacting with the CustomGPT SDK,
allowing users to manage projects, conversations, and pages through simple commands.
"""

import argparse
import sys
import logging
import os
import time
import json

from typing import Optional, List, Dict, Any, Union
from pathlib import Path
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from customgpt_client import CustomGPT
from customgpt_client.types import File

def setup_logging() -> logging.Logger:
    """
    Configure and setup logging based on environment variables.
    
    Environment Variables:
        CUSTOMGPT_CLI_LOG_LEVEL: Logging level (default: INFO)
        CUSTOMGPT_CLI_LOG_FILE: Optional file path for logging output
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Get log level from environment variable
    log_level_name = os.environ.get('CUSTOMGPT_CLI_LOG_LEVEL', 'INFO').upper()
    log_level = getattr(logging, log_level_name, logging.INFO)
    
    # Configure handlers
    handlers = []
    log_file = os.environ.get('CUSTOMGPT_CLI_LOG_FILE')
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    else:
        handlers.append(logging.StreamHandler(sys.stdout))
    
    # Setup basic configuration
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )
    
    # Get logger for this module
    logger = logging.getLogger(__name__)
    
    # Log initial configuration
    logger.debug("Log level set to: %s", log_level_name)
    if log_file:
        logger.debug("Logging to file: %s", log_file)
    
    return logger

# Setup logging once at module level
logger = setup_logging()

# Type aliases
ProjectID = str
SessionID = str
PageID = str
JsonDict = Dict[str, Any]

class CustomGPTCLI:
    def __init__(self):
        self.parser = self._create_parser()
        
    def _create_parser(self) -> argparse.ArgumentParser:
        # Create main parser
        parser = argparse.ArgumentParser(description='CustomGPT CLI Tool')
        parser.add_argument('--api-key', help='CustomGPT API Key (can also be set via CUSTOMGPT_API_KEY env var)', required=False)
        
        # Create subparsers for different commands
        subparsers = parser.add_subparsers(dest='command', help='Available commands')
        
        # Project commands
        self._add_project_commands(subparsers)
        
        # Conversation commands
        self._add_conversation_commands(subparsers)
        
        # Page commands
        self._add_page_commands(subparsers)
        
        return parser
    
    def _add_project_commands(self, subparsers):
        # Create project
        create_project = subparsers.add_parser('create-project', help='Create a new project')
        create_project.add_argument('--name', required=True, help='Project name')
        create_project.add_argument('--sitemap', help='Sitemap URL')
        create_project.add_argument('--file', help='Path to file')
        create_project.add_argument('--format', 
                        choices=['table', 'json', 'id-only'],
                        default='table',
                        help='Output format (default: table)')
        # Show project
        show_project = subparsers.add_parser('show-project', help='Show project details')
        show_project.add_argument('--project-id', required=True, help='Project ID')
        show_project.add_argument('--format', 
                                choices=['table', 'json', 'id-only'],
                                default='table',
                                help='Output format (default: table)')
                                
        # List projects
        list_projects = subparsers.add_parser('list-projects', help='List all projects')
        list_projects.add_argument('--page', type=int, default=1, help='Page number')
        list_projects.add_argument('--name-filter', help='Filter projects by name (supports regex)')
        list_projects.add_argument('--inactive-days', type=int, help='Filter projects inactive for X days')

        # Stats-based filters - both min and max
        list_projects.add_argument('--min-queries', type=int, help='Filter projects with at least X queries')
        list_projects.add_argument('--max-queries', type=int, help='Filter projects with at most X queries')
        list_projects.add_argument('--min-pages-found', type=int, help='Filter projects with at least X pages found')
        list_projects.add_argument('--max-pages-found', type=int, help='Filter projects with at most X pages found')
        list_projects.add_argument('--min-pages-crawled', type=int, help='Filter projects with at least X pages crawled')
        list_projects.add_argument('--max-pages-crawled', type=int, help='Filter projects with at most X pages crawled')
        list_projects.add_argument('--min-pages-indexed', type=int, help='Filter projects with at least X pages indexed')
        list_projects.add_argument('--max-pages-indexed', type=int, help='Filter projects with at most X pages indexed')
        list_projects.add_argument('--min-words-indexed', type=int, help='Filter projects with at least X words indexed')
        list_projects.add_argument('--max-words-indexed', type=int, help='Filter projects with at most X words indexed')
        list_projects.add_argument('--min-storage-credits', type=int, help='Filter projects with at least X storage credits used')
        list_projects.add_argument('--max-storage-credits', type=int, help='Filter projects with at most X storage credits used')
        list_projects.add_argument('--min-crawl-credits', type=int, help='Filter projects with at least X crawl credits used')
        list_projects.add_argument('--max-crawl-credits', type=int, help='Filter projects with at most X crawl credits used')
        list_projects.add_argument('--min-query-credits', type=int, help='Filter projects with at least X query credits used')
        list_projects.add_argument('--max-query-credits', type=int, help='Filter projects with at most X query credits used')
        list_projects.add_argument('--format', choices=['table', 'json', 'csv', 'id-only'], default='table', 
                                help='Output format')
                
        # Update project
        update_project = subparsers.add_parser('update-project', help='Update project')
        update_project.add_argument('--project-id', required=True, help='Project ID')
        update_project.add_argument('--name', help='New project name')
        update_project.add_argument('--is-shared', type=int, choices=[0, 1], help='Share status')
        update_project.add_argument('--format', 
                              choices=['table', 'json', 'id-only'],
                              default='table',
                              help='Output format (default: table)')
        
        # Delete projects
        delete_projects = subparsers.add_parser('delete-projects', help='Delete multiple projects')
        delete_projects.add_argument('--project-ids', required=True, help='Comma-separated list of project IDs')
        delete_projects.add_argument('--dry-run', action='store_true', help='Show what would be deleted without actually deleting')
        delete_projects.add_argument('--force', action='store_true', help='Skip confirmation prompt')
        
    def _add_conversation_commands(self, subparsers):
        # Create conversation
        create_conv = subparsers.add_parser('create-conversation', help='Create a new conversation')
        create_conv.add_argument('--project-id', required=True, help='Project ID')
        create_conv.add_argument('--name', required=True, help='Conversation name')
        
        # Send message
        send_msg = subparsers.add_parser('send-message', help='Send a message')
        send_msg.add_argument('--project-id', required=True, help='Project ID')
        send_msg.add_argument('--session-id', required=True, help='Session ID')
        send_msg.add_argument('--prompt', required=True, help='Message prompt')
        send_msg.add_argument('--stream', action='store_true', help='Enable streaming')
        send_msg.add_argument('--persona', help='Custom persona')

    def _add_page_commands(self, subparsers):
        # Get pages
        get_pages = subparsers.add_parser('get-pages', help='Get project pages')
        get_pages.add_argument('--project-id', required=True, help='Project ID')
        
        # Delete page
        delete_page = subparsers.add_parser('delete-page', help='Delete a page')
        delete_page.add_argument('--project-id', required=True, help='Project ID')
        delete_page.add_argument('--page-id', required=True, help='Page ID')
        
        # Reindex page
        reindex_page = subparsers.add_parser('reindex-page', help='Reindex a page')
        reindex_page.add_argument('--project-id', required=True, help='Project ID')
        reindex_page.add_argument('--page-id', required=True, help='Page ID')

    def _handle_rate_limit(self, response, retry_count, max_retries):
        """
        Handle rate limiting for API responses.
        
        Args:
            response: API response object
            retry_count: Current retry attempt number
            max_retries: Maximum number of retry attempts
            
        Returns:
            tuple: (should_retry, retry_after)
            - should_retry: Boolean indicating if retry should be attempted
            - retry_after: Number of seconds to wait before retry
        """
        if response.status_code == 429:
            retry_after = int(response.headers.get('Retry-After', 30))
            remaining = response.headers.get('X-RateLimit-Remaining', 'unknown')
            reset_time = response.headers.get('X-RateLimit-Reset', 'unknown')
            
            logger.warning(f"Rate limited. Remaining requests: {remaining}, "
                        f"Reset time: {reset_time}, "
                        f"Retry after: {retry_after}s")
            
            if retry_count < max_retries:
                print(f"Rate limited, waiting {retry_after} seconds before retry...")
                return True, retry_after
            
            return False, 0
        return False, 0

    def _make_api_call(self, api_func, max_retries=3, **kwargs):
        """
        Make an API call with retry logic for rate limiting.
        
        Args:
            api_func: Function to call (e.g., CustomGPT.Project.list)
            max_retries: Maximum number of retries for rate-limited requests
            **kwargs: Arguments to pass to the API function
            
        Returns:
            API response or None if failed after retries
        """
        retry_count = 0
        while retry_count <= max_retries:
            try:
                response = api_func(**kwargs)
                
                should_retry, retry_after = self._handle_rate_limit(response, retry_count, max_retries)
                if should_retry:
                    time.sleep(retry_after)
                    retry_count += 1
                    continue
                
                return response

            except Exception as e:
                logger.error(f"Exception in API call to {api_func.__name__}: {str(e)}", exc_info=True)
                return None
                
        return None

    def _get_project_stats(self, project_id, max_retries=3):
        """Get project stats using standard API call handler."""
        response = self._make_api_call(
            CustomGPT.Project.stats,
            max_retries=max_retries,
            project_id=project_id
        )
        return response.parsed.data if response and hasattr(response, 'parsed') else None

    def _get_all_projects(self, max_retries=3):
        """Fetch all projects across multiple pages using standard API call handler."""
        all_projects = []
        page = 1
        
        while True:
            response = self._make_api_call(
                CustomGPT.Project.list,
                max_retries=max_retries,
                page=page
            )
            
            if not response or not hasattr(response, 'parsed') or not response.parsed or \
            not hasattr(response.parsed, 'data') or not response.parsed.data or \
            not hasattr(response.parsed.data, 'data'):
                logger.warning(f"Incomplete or invalid response on page {page} - stopping pagination")
                break
                
            projects = response.parsed.data.data
            if not projects:
                break
                
            all_projects.extend(projects)
            
            if hasattr(response.parsed.data, 'total') and len(all_projects) >= response.parsed.data.total:
                break
                
            page += 1
            
        return all_projects

    def _delete_single_project(self, project, max_retries=3):
        """Delete a single project using standard API call handler."""
        response = self._make_api_call(
            CustomGPT.Project.delete,
            max_retries=max_retries,
            project_id=project.id
        )
        
        if not response:
            return False
            
        deleted_status = (response.parsed and 
                        hasattr(response.parsed, 'data') and 
                        response.parsed.data and 
                        hasattr(response.parsed.data, 'deleted') and 
                        response.parsed.data.deleted)
        
        if not deleted_status:
            logger.warning(f"Failed to delete project {project.id}. Response: {response}")
        
        return deleted_status

    def _parse_datetime(self, dt_value: Any) -> Optional[datetime]:
        """Safely parse a datetime value that might be a string or datetime object."""
        if isinstance(dt_value, datetime):
            return dt_value.replace(tzinfo=timezone.utc) if dt_value.tzinfo is None else dt_value
        elif isinstance(dt_value, str):
            try:
                # Try parsing ISO format
                dt = datetime.fromisoformat(dt_value.replace('Z', '+00:00'))
                return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt
            except ValueError:
                try:
                    # Try parsing common datetime formats
                    formats = [
                        '%Y-%m-%dT%H:%M:%S.%f%z',
                        '%Y-%m-%d %H:%M:%S',
                        '%Y-%m-%dT%H:%M:%S.%fZ'
                    ]
                    for fmt in formats:
                        try:
                            dt = datetime.strptime(dt_value, fmt)
                            return dt.replace(tzinfo=timezone.utc) if dt.tzinfo is None else dt
                        except ValueError:
                            continue
                    logger.warning(f"Could not parse datetime value: {dt_value}")
                    return None
                except Exception as e:
                    logger.warning(f"Error parsing datetime {dt_value}: {e}")
                    return None
        return None

    def _format_project_output(self, projects, format_type='table'):
        """
        Format project data for output.
        
        Args:
            projects: List of project objects
            format_type: Output format ('table', 'json', 'csv', or 'id-only')
            
        Returns:
            str: Formatted output string
        """
        if format_type == 'json':
            import json
            from datetime import datetime
            
            class DateTimeEncoder(json.JSONEncoder):
                def default(self, obj):
                    if isinstance(obj, datetime):
                        return obj.isoformat()
                    return super().default(obj)
            
            project_data = []
            for p in projects:
                project_dict = {
                    'id': p.id,
                    'project_name': p.project_name,
                    'created_at': p.created_at,
                    'updated_at': p.updated_at,
                    'type': p.type,
                    'is_chat_active': p.is_chat_active,
                    'is_shared': p.is_shared,
                    'sitemap_path': p.sitemap_path,
                    'stats': None
                }
                
                stats = self._get_project_stats(p.id)
                if stats:
                    project_dict['stats'] = {
                        'pages_found': getattr(stats, 'pages_found', 0),
                        'pages_crawled': getattr(stats, 'pages_crawled', 0),
                        'pages_indexed': getattr(stats, 'pages_indexed', 0),
                        'total_words_indexed': getattr(stats, 'total_words_indexed', 0),
                        'total_storage_credits_used': getattr(stats, 'total_storage_credits_used', 0),
                        'crawl_credits_used': getattr(stats, 'crawl_credits_used', 0),
                        'query_credits_used': getattr(stats, 'query_credits_used', 0),
                        'total_queries': getattr(stats, 'total_queries', 0)
                    }
                
                project_data.append(project_dict)
                
            return json.dumps(project_data, indent=2, cls=DateTimeEncoder)
        
        elif format_type == 'id-only':
            return '\n'.join(str(p.id) for p in projects)
        
        elif format_type == 'csv':
            import csv
            from io import StringIO
            from datetime import datetime
            
            # Define CSV headers including both project info and stats
            headers = [
                'ID', 'Name', 'Type', 'Created At', 'Updated At', 'Is Chat Active', 
                'Is Shared', 'Sitemap Path', 'Pages Found', 'Pages Crawled', 
                'Pages Indexed', 'Words Indexed', 'Storage Credits Used', 
                'Crawl Credits Used', 'Query Credits Used', 'Total Queries'
            ]
            
            # Create StringIO to write CSV data
            output = StringIO()
            writer = csv.writer(output)
            writer.writerow(headers)
            
            # Write data rows
            for p in projects:
                # Get stats with retry logic
                stats = self._get_project_stats(p.id)
                
                # Format timestamps
                created_at = p.created_at.isoformat() if isinstance(p.created_at, datetime) else p.created_at
                updated_at = p.updated_at.isoformat() if isinstance(p.updated_at, datetime) else p.updated_at
                
                # Base project data
                row = [
                    p.id,
                    p.project_name,
                    p.type,
                    created_at,
                    updated_at,
                    p.is_chat_active,
                    p.is_shared,
                    p.sitemap_path or ''
                ]
                
                # Add stats data if available
                if stats:
                    row.extend([
                        getattr(stats, 'pages_found', 0),
                        getattr(stats, 'pages_crawled', 0),
                        getattr(stats, 'pages_indexed', 0),
                        getattr(stats, 'total_words_indexed', 0),
                        getattr(stats, 'total_storage_credits_used', 0),
                        getattr(stats, 'crawl_credits_used', 0),
                        getattr(stats, 'query_credits_used', 0),
                        getattr(stats, 'total_queries', 0)
                    ])
                else:
                    row.extend(['N/A'] * 8)  # Add N/A for missing stats
                
                writer.writerow(row)
            
            return output.getvalue()
        
        else:  # table format
            from tabulate import tabulate
            headers = [
                'ID', 'Name', 'Created At', 'Updated At', 'Type',
                'Pages Found', 'Pages Crawled', 'Pages Indexed',
                'Words Indexed', 'Storage Credits', 'Crawl Credits',
                'Query Credits', 'Total Queries'
            ]
            rows = []
            for p in projects:
                stats = self._get_project_stats(p.id)  # Use the retry-enabled method
                if stats:
                    stats_values = [
                        getattr(stats, 'pages_found', 'N/A'),
                        getattr(stats, 'pages_crawled', 'N/A'),
                        getattr(stats, 'pages_indexed', 'N/A'),
                        getattr(stats, 'total_words_indexed', 'N/A'),
                        getattr(stats, 'total_storage_credits_used', 'N/A'),
                        getattr(stats, 'crawl_credits_used', 'N/A'),
                        getattr(stats, 'query_credits_used', 'N/A'),
                        getattr(stats, 'total_queries', 'N/A')
                    ]
                else:
                    stats_values = ['N/A'] * 8
                
                rows.append([
                    p.id, 
                    p.project_name, 
                    p.created_at, 
                    p.updated_at, 
                    p.type,
                    *stats_values
                ])
            return tabulate(rows, headers=headers, tablefmt='grid')

    def _filter_projects(self, projects, name_filter=None, inactive_days=None, **stats_filters):
        """
        Filter projects based on various criteria including detailed stats.
        
        Args:
            projects: List of projects to filter
            name_filter: Regex pattern to filter project names
            inactive_days: Filter projects inactive for X days
            **stats_filters: Stats-based filters including:
                - min_queries/max_queries: Filter by number of queries
                - min_pages_found/max_pages_found: Filter by pages found
                - min_pages_crawled/max_pages_crawled: Filter by pages crawled
                - min_pages_indexed/max_pages_indexed: Filter by pages indexed
                - min_words_indexed/max_words_indexed: Filter by words indexed
                - min_storage_credits/max_storage_credits: Filter by storage credits
                - min_crawl_credits/max_crawl_credits: Filter by crawl credits
                - min_query_credits/max_query_credits: Filter by query credits
        
        Returns:
            list: Filtered list of projects
        """
        import re

        filtered_projects = projects

        if name_filter:
            pattern = re.compile(name_filter, re.IGNORECASE)
            filtered_projects = [p for p in filtered_projects 
                            if pattern.search(p.project_name)]

        if inactive_days is not None:
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=inactive_days)
            filtered_projects = [
                p for p in filtered_projects 
                if (parsed_date := self._parse_datetime(p.updated_at)) is not None 
                and parsed_date < cutoff_date
            ]

        # Stats-based filtering
        stat_field_mappings = {
            'min_queries': ('total_queries', 0, float('inf')),
            'max_queries': ('total_queries', 0, float('inf')),
            'min_pages_found': ('pages_found', 0, float('inf')),
            'max_pages_found': ('pages_found', 0, float('inf')),
            'min_pages_crawled': ('pages_crawled', 0, float('inf')),
            'max_pages_crawled': ('pages_crawled', 0, float('inf')),
            'min_pages_indexed': ('pages_indexed', 0, float('inf')),
            'max_pages_indexed': ('pages_indexed', 0, float('inf')),
            'min_words_indexed': ('total_words_indexed', 0, float('inf')),
            'max_words_indexed': ('total_words_indexed', 0, float('inf')),
            'min_storage_credits': ('total_storage_credits_used', 0, float('inf')),
            'max_storage_credits': ('total_storage_credits_used', 0, float('inf')),
            'min_crawl_credits': ('crawl_credits_used', 0, float('inf')),
            'max_crawl_credits': ('crawl_credits_used', 0, float('inf')),
            'min_query_credits': ('query_credits_used', 0, float('inf')),
            'max_query_credits': ('query_credits_used', 0, float('inf')),
        }

        # Remove None values from stats_filters
        active_filters = {k: v for k, v in stats_filters.items() if v is not None}
        
        if active_filters:
            filtered_projects_with_stats = []
            for project in filtered_projects:
                try:
                    stats = self._get_project_stats(project.id)
                    if not stats:
                        continue
                        
                    include_project = True
                    
                    # Track min and max values for each stat field
                    stat_ranges = {}
                    
                    # First pass: collect min/max values for each stat field
                    for filter_name, filter_value in active_filters.items():
                        if filter_name not in stat_field_mappings:
                            continue
                            
                        stat_field, min_default, max_default = stat_field_mappings[filter_name]
                        stat_value = getattr(stats, stat_field, None)
                        
                        if stat_value is None:
                            include_project = False
                            break
                            
                        # Initialize or update stat ranges
                        if stat_field not in stat_ranges:
                            stat_ranges[stat_field] = {
                                'min': min_default,
                                'max': max_default,
                                'value': stat_value
                            }
                        
                        # Update min/max bounds based on filters
                        if filter_name.startswith('min_'):
                            stat_ranges[stat_field]['min'] = max(stat_ranges[stat_field]['min'], filter_value)
                        elif filter_name.startswith('max_'):
                            stat_ranges[stat_field]['max'] = min(stat_ranges[stat_field]['max'], filter_value)
                    
                    # Second pass: check if value is within min/max range for each stat
                    for stat_field, ranges in stat_ranges.items():
                        if not (ranges['min'] <= ranges['value'] <= ranges['max']):
                            include_project = False
                            break
                    
                    if include_project:
                        filtered_projects_with_stats.append(project)
                except Exception as e:
                    logger.warning(f"Could not get stats for project {project.id}: {e}")
            
            filtered_projects = filtered_projects_with_stats

        return filtered_projects

    def _delete_single_project(self, project, max_retries=3):
        """
        Delete a single project with retry logic for rate limiting.
        
        Args:
            project: Project object containing id and project_name
            max_retries: Maximum number of retries for rate-limited requests
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        retry_count = 0
        while retry_count <= max_retries:
            try:
                response = CustomGPT.Project.delete(project_id=project.id)
                
                # Log the response
                logger.debug(f"Delete response for project {project.id}:")
                logger.debug(f"Response status code: {response.status_code}")
                logger.debug(f"Response headers: {response.headers}")
                logger.debug(f"Response parsed: {response.parsed}")
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 30))
                    remaining = response.headers.get('X-RateLimit-Remaining', 'unknown')
                    reset_time = response.headers.get('X-RateLimit-Reset', 'unknown')
                    
                    logger.warning(f"Rate limited when deleting project {project.id}. "
                                f"Remaining requests: {remaining}, "
                                f"Reset time: {reset_time}, "
                                f"Retry after: {retry_after}s")
                    
                    if retry_count < max_retries:
                        logger.warning(f"Rate limited, waiting {retry_after} seconds before retry...")
                        time.sleep(retry_after)
                        retry_count += 1
                        continue
                    return False
                
                # Get deletion status
                deleted_status = (response.parsed and 
                                hasattr(response.parsed, 'data') and 
                                response.parsed.data and 
                                hasattr(response.parsed.data, 'deleted') and 
                                response.parsed.data.deleted)
                
                if not deleted_status:
                    logger.warning(f"Failed to delete project {project.id}. Response: {response}")
                
                return deleted_status

            except Exception as e:
                logger.error(f"Exception deleting project {project.id}: {str(e)}", exc_info=True)
                return False

    def _handle_create_project(self, args):
        """
        Handle the create-project command with improved error handling and output formatting.
        
        Args:
            args: Parsed command line arguments
            
        Returns:
            None - prints output to stdout
        """
        try:
            # Validate input requirements
            if not args.sitemap and not args.file:
                print("Error: Either --sitemap or --file must be provided")
                sys.exit(1)
                
            if args.sitemap and args.file:
                print("Error: Cannot provide both --sitemap and --file. Please choose one.")
                sys.exit(1)
                
            # Prepare creation arguments
            create_args = {'project_name': args.name}
            
            # Handle sitemap path
            if args.sitemap:
                create_args['sitemap_path'] = args.sitemap
                logger.debug(f"Creating project with sitemap: {args.sitemap}")
                
            # Handle file upload
            elif args.file:
                try:
                    file_path = Path(args.file)
                    if not file_path.exists():
                        print(f"Error: File not found: {args.file}")
                        sys.exit(1)
                        
                    if not file_path.is_file():
                        print(f"Error: Not a file: {args.file}")
                        sys.exit(1)
                        
                    with open(file_path, 'rb') as f:
                        file_content = f.read()
                    create_args['file'] = File(payload=file_content, file_name=str(file_path.name))
                    logger.debug(f"Creating project with file: {file_path.name}")
                    
                except Exception as e:
                    print(f"Error reading file {args.file}: {str(e)}")
                    logger.error(f"File read error", exc_info=True)
                    sys.exit(1)
            
            # Make API call with retry logic
            result = self._make_api_call(CustomGPT.Project.create, **create_args)
            
            if not result or not hasattr(result, 'parsed'):
                print("Error: Failed to create project - invalid API response")
                sys.exit(1)
                
            # Check for error response
            if hasattr(result, 'status_code') and result.status_code >= 400:
                error_msg = "Unknown error"
                if hasattr(result.parsed, 'message'):
                    error_msg = result.parsed.message
                elif hasattr(result.parsed, 'error'):
                    error_msg = result.parsed.error
                    
                print(f"Error creating project: {error_msg}")
                sys.exit(1)
                
            # Get response JSON content
            try:
                import json
                response_data = json.loads(result.content)
            except json.JSONDecodeError:
                print("Error: Invalid JSON response from API")
                sys.exit(1)
                
            if 'data' not in response_data:
                print("Error: Unexpected API response format - missing data field")
                sys.exit(1)
                
            project_data = response_data['data']
            
            # Format output based on requested format
            if hasattr(args, 'format'):
                if args.format == 'id-only':
                    print(project_data.get('id', 'N/A'))
                elif args.format == 'json':
                    # For JSON output, return the complete response data
                    print(json.dumps(response_data, indent=2))
                else:  # default format - human readable
                    print(f"Successfully created project:")
                    print(f"  ID: {project_data.get('id', 'N/A')}")
                    print(f"  Name: {project_data.get('project_name', 'N/A')}")
                    print(f"  Type: {project_data.get('type', 'N/A')}")
                    if project_data.get('sitemap_path'):
                        print(f"  Sitemap: {project_data['sitemap_path']}")
                    print(f"  Created at: {project_data.get('created_at', 'N/A')}")
            else:
                # Basic output if format not specified
                print(f"Successfully created project {project_data.get('id', 'N/A')}: {project_data.get('project_name', 'N/A')}")
                
        except Exception as e:
            logger.error("Unexpected error in create project", exc_info=True)
            print(f"Error: {str(e)}")
            sys.exit(1)

    def _handle_show_project(self, args):
        """
        Handle the show-project command with output formatting.
        
        Args:
            args: Parsed command line arguments
        """
        try:
            result = self._make_api_call(CustomGPT.Project.get, project_id=args.project_id)
            
            if not result:
                print("Error: Failed to get project - no API response")
                sys.exit(1)
                
            # Check for error response
            if result.status_code >= 400:
                error_msg = "Unknown error"
                try:
                    response_data = json.loads(result.content)
                    error_msg = response_data.get('message', response_data.get('error', 'Unknown error'))
                except:
                    pass
                print(f"Error getting project: {error_msg}")
                sys.exit(1)
                
            # Get response JSON content
            try:
                response_data = json.loads(result.content)
            except json.JSONDecodeError:
                print("Error: Invalid JSON response from API")
                sys.exit(1)
                
            if 'data' not in response_data:
                print("Error: Unexpected API response format - missing data field")
                sys.exit(1)
                
            project_data = response_data['data']
            
            # Format output based on requested format
            if args.format == 'id-only':
                print(project_data.get('id', 'N/A'))
            elif args.format == 'json':
                # For JSON output, return the complete response data
                print(json.dumps(response_data, indent=2))
            else:  # default table format
                print("Project Details:")
                
                # Group the fields by category for better organization
                code_fields = ['embed_code', 'live_chat_code']  # Fields containing code snippets
                url_fields = ['shareable_link']  # Fields containing URLs
                skip_fields = []  # Fields to skip if needed
                
                # First print regular fields (not code or urls)
                for key, value in sorted(project_data.items()):
                    if key not in code_fields + url_fields + skip_fields:
                        # Convert boolean values to Yes/No for better readability
                        if isinstance(value, bool):
                            value = "Yes" if value else "No"
                        # Handle null values
                        elif value is None:
                            value = "N/A"
                            
                        # Format key for display (convert snake_case to Title Case)
                        display_key = key.replace('_', ' ').title()
                        print(f"  {display_key}: {value}")
                
                # Then print URL fields
                url_values = [(key, value) for key, value in project_data.items() 
                            if key in url_fields and value]
                if url_values:
                    print("\nShare Information:")
                    for key, value in url_values:
                        display_key = key.replace('_', ' ').title()
                        print(f"  {display_key}: {value}")
                
                # Finally print code fields
                code_values = [(key, value) for key, value in project_data.items() 
                            if key in code_fields and value]
                if code_values:
                    for key, value in code_values:
                        print(f"\n{key.replace('_', ' ').title()}:")
                        print(f"  {value}")
                
        except Exception as e:
            logger.error("Unexpected error in show project", exc_info=True)
            print(f"Error: {str(e)}")
            sys.exit(1)
            
    def _handle_update_project(self, args):
        """
        Handle the update-project command with improved error handling and output formatting.
        
        Args:
            args: Parsed command line arguments
        """
        try:
            # Prepare update arguments
            update_args = {'project_id': args.project_id}
            if args.name:
                update_args['project_name'] = args.name
            if args.is_shared is not None:
                update_args['is_shared'] = args.is_shared
                
            # Make API call with retry logic
            result = self._make_api_call(CustomGPT.Project.update, **update_args)
            
            if not result:
                print("Error: Failed to update project - no API response")
                sys.exit(1)
                
            # Check for error response
            if result.status_code >= 400:
                error_msg = "Unknown error"
                try:
                    response_data = json.loads(result.content)
                    error_msg = response_data.get('message', response_data.get('error', 'Unknown error'))
                except:
                    pass
                print(f"Error updating project: {error_msg}")
                sys.exit(1)
                
            # Get response JSON content
            try:
                response_data = json.loads(result.content)
            except json.JSONDecodeError:
                print("Error: Invalid JSON response from API")
                sys.exit(1)
                
            if 'data' not in response_data:
                print("Error: Unexpected API response format - missing data field")
                sys.exit(1)
                
            project_data = response_data['data']
            
            # Format output based on requested format
            if args.format == 'id-only':
                print(project_data.get('id', 'N/A'))
            elif args.format == 'json':
                # For JSON output, return the complete response data
                print(json.dumps(response_data, indent=2))
            else:  # default table format
                print(f"Successfully updated project:")
                print(f"  ID: {project_data.get('id', 'N/A')}")
                print(f"  Name: {project_data.get('project_name', 'N/A')}")
                print(f"  Type: {project_data.get('type', 'N/A')}")
                print(f"  Is Shared: {project_data.get('is_shared', 'N/A')}")
                print(f"  Updated at: {project_data.get('updated_at', 'N/A')}")
                
        except Exception as e:
            logger.error("Unexpected error in update project", exc_info=True)
            print(f"Error: {str(e)}")
            sys.exit(1)
    
    def _handle_project_commands(self, args):
        """Handle all project-related commands."""
        if args.command == 'create-project':
            self._handle_create_project(args)
        elif args.command == 'show-project':
            self._handle_show_project(args)             
        elif args.command == 'list-projects':
            all_projects = self._get_all_projects()
            
            if not all_projects:
                print("No projects found or unable to retrieve projects")
                return
                
            try:
                filtered_projects = self._filter_projects(
                    all_projects,
                    name_filter=args.name_filter,
                    inactive_days=args.inactive_days,
                    min_queries=args.min_queries,
                    max_queries=args.max_queries,
                    min_pages_found=args.min_pages_found,
                    min_pages_crawled=args.min_pages_crawled,
                    min_pages_indexed=args.min_pages_indexed,
                    min_words_indexed=args.min_words_indexed,
                    min_storage_credits=args.min_storage_credits,
                    min_crawl_credits=args.min_crawl_credits,
                    min_query_credits=args.min_query_credits
                )
                print(self._format_project_output(filtered_projects, args.format))
            except Exception as e:
                logger.warning(f"Error processing projects: {str(e)}")
                print("Error processing projects - displaying unfiltered results:")
                print(self._format_project_output(all_projects, args.format))
                
        elif args.command == 'update-project':
            self._handle_update_project(args)
                
        elif args.command == 'delete-projects':
            # Get projects to delete
            projects_to_delete = []
            
            if args.project_ids:
                project_ids = [int(id.strip()) for id in args.project_ids.split(',')]
                all_projects = self._get_all_projects()
                projects_to_delete = [p for p in all_projects if p.id in project_ids]
                
                # Log which IDs were not found
                found_ids = {p.id for p in projects_to_delete}
                not_found_ids = set(project_ids) - found_ids
                if not_found_ids:
                    print(f"Warning: Could not find projects with IDs: {', '.join(str(id) for id in not_found_ids)}")
            
            else:
                print("Error: Must provide --project-ids")
                return

            if not projects_to_delete:
                print("No projects found matching the criteria")
                return

            # Show what will be deleted
            print("\nProjects that will be deleted:")
            print(self._format_project_output(projects_to_delete))
            
            if args.dry_run:
                return
            
            if not args.force:
                confirm = input(f"\nAre you sure you want to delete {len(projects_to_delete)} "
                            f"projects? (yes/no): ")
                if confirm.lower() != 'yes':
                    print("Operation cancelled")
                    return

            # Perform deletion
            success_count = 0
            error_count = 0
            
            for project in projects_to_delete:
                success = self._delete_single_project(project)
                print(f"Deleted project {project.id}: {project.project_name} -> Status: {'success' if success else 'failed'}")
                if success:
                    success_count += 1
                else:
                    error_count += 1

            print(f"\nDeletion complete: {success_count} succeeded, {error_count} failed")

    def _handle_conversation_commands(self, args):
        """Handle all conversation-related commands."""
        if args.command == 'create-conversation':
            result = self._make_api_call(
                CustomGPT.Conversation.create,
                project_id=args.project_id,
                name=args.name
            )
            print(result)
            
        elif args.command == 'send-message':
            api_args = {
                'project_id': args.project_id,
                'session_id': args.session_id,
                'prompt': args.prompt,
                'stream': args.stream
            }
            if args.persona:
                api_args['custom_persona'] = args.persona
                
            result = self._make_api_call(CustomGPT.Conversation.send, **api_args)
            if args.stream and result:
                for event in result.events():
                    print(event.data)
            else:
                print(result)

    def _handle_page_commands(self, args):
        """Handle all page-related commands."""
        if args.command == 'get-pages':
            result = self._make_api_call(
                CustomGPT.Page.get,
                project_id=args.project_id
            )
            print(result)
            
        elif args.command == 'delete-page':
            result = self._make_api_call(
                CustomGPT.Page.delete,
                project_id=args.project_id,
                page_id=args.page_id
            )
            print(result)
            
        elif args.command == 'reindex-page':
            result = self._make_api_call(
                CustomGPT.Page.reindex,
                project_id=args.project_id,
                page_id=args.page_id
            )
            print(result)
                                            
    def run(self):
        args = self.parser.parse_args()
        
        if not args.command:
            self.parser.print_help()
            return
            
        # Get API key from argument or environment variable
        api_key = args.api_key or os.environ.get('CUSTOMGPT_API_KEY')
        if not api_key:
            print("Error: API key must be provided via --api-key argument or CUSTOMGPT_API_KEY environment variable")
            sys.exit(1)
            
        # Set API key
        CustomGPT.api_key = api_key
        
        # Handle commands by category
        if args.command in ['create-project', 'show-project', 'list-projects', 'update-project', 'delete-projects']:
            self._handle_project_commands(args)
        elif args.command in ['create-conversation', 'send-message']:
            self._handle_conversation_commands(args)
        elif args.command in ['get-pages', 'delete-page', 'reindex-page']:
            self._handle_page_commands(args)

def main():
    cli = CustomGPTCLI()
    cli.run()

if __name__ == "__main__":
    main()
