import PySimpleGUI as sg

from todo_list.interfaces.views import IView


class TodoListView(IView):
    layout = []


# class IssueManagementView(IView):
#     issue_service: IIssueService
#     view_factory: IViewFactory

#     def move_issue(self, issue: Issue, from_list: IssueList, to_list: IssueList):
#         from_list.remove(issue)
#         to_list.append(issue)

#     def run(self):
#         event = None
#         window = None
#         active_issues, deleted_issues = self.issue_service.load_lists()
#         while event not in [
#             IssueManagementViewEvents.SAVE,
#             IssueManagementViewEvents.CANCEL,
#             sg.WIN_CLOSED,
#         ]:
#             if window is None:
#                 window = sg.Window(self.title, self.layout, size=self.size)
#             window[IssueManagementViewKeys.ACTIVE_ISSUES].update(active_issues.issues)
#             window[IssueManagementViewKeys.DELETED_ISSUES].update(deleted_issues.issues)
#             event, values = window.read()
#             match event:
#                 case [IssueManagementViewEvents.NEW]:
#                     window = window.close()
#                     active_issues = self.view_factory.make_new_issue_view().run()
#                 case [IssueManagementViewEvents.DELETE]:
#                     self.move_issue(
#                         issue=values[IssueManagementViewKeys.ACTIVE_ISSUES],
#                         from_list=active_issues,
#                         to_list=deleted_issues,
#                     )
#                 case [IssueManagementViewEvents.RESTORE]:
#                     active_issues, deleted_issues = self.issue_service.load_lists()
#                 case [IssueManagementViewEvents.SAVE]:
#                     window = window.close()
#                     self.issue_service.save_all_lists(active_issues, deleted_issues)
#                     return event
#                 case [IssueManagementViewEvents.CANCEL | sg.WIN_CLOSED]:
#                     return IssueManagementViewEvents.CANCEL

#     def __init__(self, issue_service: IIssueService, view_factory: IViewFactory):
#         self.issue_service = issue_service
#         self.view_factory = view_factory
#         self.title = "Time Tracking - Manage Issues"
#         self.size = (550, 775)
#         self.layout = [
#             [
#                 sg.Text("Active Issues", size=(30, 1)),
#                 sg.Text(EMPTY, size=(5, 1)),
#                 sg.Text("Deleted Issues", size=(30, 1)),
#             ],
#             [
#                 sg.Listbox(
#                     issue_service.load_active_issues(),
#                     key=IssueManagementViewKeys.ACTIVE_ISSUES,
#                     size=(30, 40),
#                 ),
#                 sg.Frame(
#                     EMPTY,
#                     [
#                         [
#                             sg.Button(
#                                 " + ",
#                                 key=IssueManagementViewEvents.NEW,
#                                 size=(5, 1),
#                                 tooltip="Create New Issue(s)",
#                             )
#                         ],
#                         [
#                             sg.Button(
#                                 " <- ",
#                                 key=IssueManagementViewEvents.RESTORE,
#                                 size=(5, 1),
#                                 tooltip="Restore Selected Issues",
#                             )
#                         ],
#                         [
#                             sg.Button(
#                                 " -> ",
#                                 key=IssueManagementViewEvents.DELETE,
#                                 size=(5, 1),
#                                 tooltip="Delete Selected Issues",
#                             )
#                         ],
#                     ],
#                 ),
#                 sg.Listbox(
#                     issue_service.load_deleted_issues(),
#                     key=IssueManagementViewKeys.DELETED_ISSUES,
#                     size=(30, 40),
#                 ),
#             ],
#             [
#                 sg.Button("Save and Close", key=IssueManagementViewEvents.SAVE),
#                 sg.Cancel(key=IssueManagementViewEvents.CANCEL),
#             ],
#         ]
