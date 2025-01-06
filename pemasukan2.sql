USE [bukukas]
GO

/****** Object:  Table [dbo].[pemasukan2]    Script Date: 06/01/2025 21:42:20 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[pemasukan2](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[amount] [decimal](18, 2) NOT NULL,
	[description] [nvarchar](255) NOT NULL,
	[created_at] [datetime] NULL DEFAULT (getdate()),
	[user_id] [int] NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]

GO

ALTER TABLE [dbo].[pemasukan2]  WITH CHECK ADD FOREIGN KEY([user_id])
REFERENCES [dbo].[users] ([id])
GO


